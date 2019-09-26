import os
from flask import current_app, _app_ctx_stack, Blueprint, request, redirect, url_for, Response, render_template
from .utils import DEFAULT_TEMPLATE_HOME, DEFAULT_TEMPLATE_ABOUT, check_config, PACKAGE_NAME, id_from_uri
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
            "rofr": self.rofr
            }

        self.blueprint.add_url_rule(os.path.join("/",reg.path), context_vars["dataset_home_endpoint"], self.show_rofr) #strict_slashes=False
        self.blueprint.context_processor(lambda: context_vars)

        app.register_blueprint(self.blueprint, url_prefix='/dataset')
    

    def show_about(self):
        return render_template(DEFAULT_TEMPLATE_ABOUT)

    def show_rofr(self):
        #assuming single rofr for now
        register = self.rofr

        # sort of a temp parent to register to run through the render pipeline
        dummy_reg = RegisterOfRegisters("http://dummydata/root",[register])
        view, format = self.get_view_and_format(request, dummy_reg)


        return format.render_response(self.rofr.base_uri, view, dummy_reg, request)


    def show_register_object(self, id):
        reg_endpoint = request.endpoint.split(".", 1)[1]
        register = self.register_for_endpoint(reg_endpoint)

        view, format = self.get_view_and_format(request, register)
        uri = register.get_uri_for(id)

        page = request.args.get('page')
        per_page = request.args.get('per_page')
        extras = {
            "page": int(page) if page else 1,
            "per_page": int(per_page) if per_page else 20
        }

        return format.render_response(uri, view, register, request, **extras)

    # this function is here to allow linkdata.gov.au redirect to be cleaner
    def show_object(self):

        raise NotImplementedError(f"Need to pass through the params, header, and extensions")

        uri = request.args.get('uri', type=str, default=None)
        register = register_for_uri(uri)
        if register:
            id = id_from_uri(uri)
            response = redirect(url_for(f".{register.get_route_endpoint()}", id=id), 302)
        else:
            rofr = rofr_for_uri(uri)
            if rofr:
                response = redirect(url_for(f".{rofr.get_route_endpoint()}"), 302)
        
        if not response:
            raise NotImplementedError(f"Unknown URI: '{uri}'")

        response.headers = request.headers

    def register_for_uri(self, uri):
        return next((reg for reg in self.registers if reg.can_resolve_uri(uri)), None)

    def register_for_endpoint(self, endpoint):
        return next((reg for reg in self.registers if reg.get_route_endpoint() == endpoint), None)

    def rofr_for_uri(self, uri):
        return next((reg for reg in self.registers if isinstance(reg, RegisterOfRegisters) and reg.get_route_endpoint() == endpoint), None)

    def get_view_and_format(self, request, register):
        view_key = request.args.get('_view')
        format_key = request.args.get('_format')

        view = register.get_view(
            view_key) if view_key else register.get_default_view()
        if view == None:
            raise NotImplementedError(
                "No view exists of type '{}' on the requested object".format(view_key))

        format = view.get_format(
            format_key) if format_key else view.get_default_format()
        if format == None:
            raise NotImplementedError(
                "No format exists of type '{}' on the requested view".format(format_key))

        return view, format