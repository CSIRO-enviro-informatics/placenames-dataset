import os
import accept_types
from flask import current_app, _app_ctx_stack, Blueprint, request, redirect, url_for, Response, render_template
from .utils import DEFAULT_TEMPLATE_HOME, DEFAULT_TEMPLATE_ABOUT, check_config, PACKAGE_NAME, id_from_uri, base_from_uri
from .rofr import RegisterOfRegisters


class MyLDApi(object):
    def __init__(self, app, dataset_name, dataset_uri, registers):
        """Represents a single dataset, which is made up of many registers"""
        self.app = app
        self.registers = registers
        self.dataset_name = dataset_name
        self.dataset_uri = dataset_uri
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("APP_TITLE", "MYLDAPI App")
        app.config.setdefault("CITATION_TEMPLATE","{type} {id}. {type} from the {dataset}. {uri}")

        self.rofr = RegisterOfRegisters(self.dataset_uri, self.registers[:], name=self.dataset_name)
        self.registers.append(self.rofr)

        self.blueprint = Blueprint(PACKAGE_NAME, __name__,
                                   static_folder="static",
                                   template_folder="templates",
                                   static_url_path=f"/{PACKAGE_NAME}/static")

        self.blueprint.add_url_rule("/object", "object", self.show_object)
        self.blueprint.add_url_rule("/about", "about", self.show_about)

        for reg in self.registers:
            self.blueprint.add_url_rule(os.path.join("/", reg.path, "<id>"), reg.get_route_endpoint(), self.show_register_object)

        # self.blueprint.add_url_rule(os.path.join("/", reg.path), "home", self.show_home)

        context_vars = {
            "dataset_name": self.dataset_name,
            "dataset_home_endpoint": "dataset_root", #self.rofr.get_route_endpoint()
            "rofr": self.rofr,
            "id_from_uri": id_from_uri,
            "base_from_uri": base_from_uri
            }

        self.blueprint.add_url_rule(os.path.join("/",reg.path), context_vars["dataset_home_endpoint"], self.show_rofr) #strict_slashes=False
        self.blueprint.context_processor(lambda: context_vars)

        app.register_blueprint(self.blueprint)
    

    def show_about(self):
        return render_template(DEFAULT_TEMPLATE_ABOUT)

    def show_rofr(self):
        #assuming single rofr for now
        register = self.rofr

        # sort of a temp parent to register to run through the render pipeline
        dummy_reg = RegisterOfRegisters("http://dummydata/root",[register])
        view, format, lang = self.get_view_format_and_lang(request, dummy_reg)

        return format.render_response(self.rofr.get_uri(), view, lang, dummy_reg, request)


    def show_register_object(self, id):
        reg_endpoint = request.endpoint.split(".", 1)[1]
        register = self.register_for_endpoint(reg_endpoint)

        view, format, lang = self.get_view_format_and_lang(request, register)
        uri = register.get_uri_for(id)

        page = request.args.get('page')
        per_page = request.args.get('per_page')
        extras = {
            "page": int(page) if page else 1,
            "per_page": int(per_page) if per_page else 20,
        }

        return format.render_response(uri, view, lang, register, request, **extras)
        


    # this function is here to allow linkdata.gov.au redirect to be cleaner
    def show_object(self):
        uri = request.args.get('uri', type=str, default=None)

        params = request.args.copy()
        del params['uri']

        register = self.register_for_uri(uri)
        if register:
            id = id_from_uri(uri)
            response = redirect(url_for(f".{register.get_route_endpoint()}", id=id, **params), 302, Response=None)
        else:
            rofr = rofr_for_uri(uri)
            if rofr:
                response = redirect(url_for(f".{rofr.get_route_endpoint()}", **params), 302)
        
        if not response:
            raise NotImplementedError(f"Unknown URI: '{uri}'")

        # I think headers are passed through on redirects...?
        # Might need to pass through extensions though? if I use them

        return response

    def register_for_uri(self, uri):
        return next((reg for reg in self.registers if reg.can_resolve_uri(uri)), None)

    def register_for_endpoint(self, endpoint):
        return next((reg for reg in self.registers if reg.get_route_endpoint() == endpoint), None)

    def rofr_for_uri(self, uri):
        return next((reg for reg in self.registers if isinstance(reg, RegisterOfRegisters) and reg.get_route_endpoint() == endpoint), None)

    def get_view_format_and_lang(self, request, register):
        """ 
        Determine the view, format and language to use based on the request.
        Query Parameters have priority over content-neg
        """
        view_key = request.args.get('_view')
        format_key = request.args.get('_format')
        language_key = request.args.get('_lang')

        if view_key:
            view = register.get_view(view_key)            
            if view == None: 
                raise NotImplementedError(f"No view exists of type '{view_key}' on the requested object")
        elif 'Accept-Profile' in request.headers:
            view = self._get_best_accept_view_by_content_neg(request, register)
            #i think if we specified a view, and it isn't found, error, not provide default
            if view == None: 
                raise NotImplementedError(f"No view match for the Accept-Profile headers exists")
        else:
            view = register.get_default_view()

        if format_key:            
            format = view.get_format(format_key)
            if format == None:
                raise NotImplementedError(f"No format exists of type '{format_key}' on the requested view")
        elif 'Accept' in request.headers:
            format = self._get_best_accept_mediatype_by_content_neg(request, view)
            #i think if we specified a format, and it isn't found, error, not provide default
            if format == None:
                raise NotImplementedError(f"No format matches the Accept header sent for the requested view")
        else:
            format = view.get_default_format()

        if language_key:            
            if language_key in view.languages:
                language = language_key
            else:
                raise NotImplementedError(f"No language exists for '{language_key}' on the requested view")
        elif 'Accept-Language' in request.headers:
            language = self._get_best_accept_language_by_content_neg(request, view)
            #i think if we specified a language, and it isn't found, error, not provide default
            if language == None:
                raise NotImplementedError(f"No language match for Accept-Language header on the requested view")
        else:
            language = view.get_default_language()

        return view, format, language

    def _get_accept_profiles_in_order(self, request):
        """
        Reads an Accept-Profile HTTP header and returns an array of Profile URIs in descending weighted order

        :return: List of URIs of accept profiles in descending request order
        :rtype: list
        """
        if not 'Accept-Profile' in request.headers:
            return []

        try:
            # split the header into individual URIs, with weights still attached
            profiles = request.headers['Accept-Profile'].split(',')
            # remove <, >, and \s
            profiles = [x.replace('<', '').replace('>', '').replace(' ', '').strip() for x in profiles]

            # split off any weights and sort by them with default weight = 1
            profiles = [(float(x.split(';')[1].replace('q=', '')) if len(x.split(';')) == 2 else 1, x.split(';')[0]) for x in profiles]

            # sort profiles by weight, heaviest first
            profiles.sort(reverse=True)

            return [x[1] for x in profiles]
        except Exception as e:
            raise ValueError(f"You have requested a profile using an Accept-Profile header that is incorrectly formatted: Accept-Profile='{request.headers['Accept-Profile']}'")

    def _get_best_accept_view_by_content_neg(self, request, register):
        profiles_uris = self._get_accept_profiles_in_order(request)

        for preferred_profile in profiles_uris:
            view = next((v for v in register.views if v.profile_uri == preferred_profile), None)
            if view:
                return view

        return None 

    def _get_best_accept_mediatype_by_content_neg(self, request, view):
        available_types = [media_type for f in view.formats for media_type in f.media_types ]
        best_match = accept_types.get_best_match(request.headers['Accept'], available_types)

        #prioritise default media types, then check others
        format = next((f for f in view.formats if f.default_media_type() == best_match), None)
        if not format:
            format = next((f for f in view.formats if best_match in f.media_types), None)    

        return format

    def _get_accept_languages_in_order(self, request):
        """
        Reads an Accept HTTP header and returns an array of Media Type string in descending weighted order

        :return: List of URIs of accept profiles in descending request order
        :rtype: list
        """
        if not 'Accept-Language' in request.headers:
            return []
        try:
            # split the header into individual URIs, with weights still attached
            profiles = request.headers['Accept-Language'].split(',')
            # remove \s
            profiles = [x.replace(' ', '').strip() for x in profiles]

            # split off any weights and sort by them with default weight = 1
            profiles = [(float(x.split(';')[1].replace('q=', '')) if len(x.split(';')) == 2 else 1, x.split(';')[0]) for x in profiles]

            # sort profiles by weight, heaviest first
            profiles.sort(reverse=True)

            return[x[1] for x in profiles]
        except Exception as e:
            raise ValueError(
                f"You have requested a language using an Accept-Language header that is incorrectly formatted. Accept-Language='{request.headers['Accept-Language']}'")

    def _get_best_accept_language_by_content_neg(self, request, view):
        languages_requested = self._get_accept_languages_in_order(request)

        for language in languages_requested:
            lang = next((l for l in view.languages if l == language), None)
            if lang:
                return lang

        return None  # if no match found
