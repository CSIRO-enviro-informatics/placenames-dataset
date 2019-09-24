import os
from flask import current_app, _app_ctx_stack, Blueprint, request, redirect, url_for, Response, render_template
from .utils import DEFAULT_TEMPLATE_HOME, DEFAULT_TEMPLATE_ABOUT, check_config, PACKAGE_NAME
from .rofr import RegisterOfRegisters

class MyLDApi(object):
    def __init__(self, app=None, objects=[]):
        self.app = app
        self.objects = objects
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        check_config('APP_TITLE', app)
        # Not sure DATASET_NAME is a good config var. I would like to tie it to RofR maybe? but gets used in citation stuff
        check_config('DATASET_NAME', app)
        check_config('DATASET_URI', app)
        app.config.setdefault("CITATION_TEMPLATE", "{type} {id}. {type} from the {dataset}. {uri}")

        # self.rofr = RegisterOfRegisters(app.config["DATASET_URI"], self.objects[:])        
        # self.objects.append(self.rofr)

        self.blueprint = Blueprint(PACKAGE_NAME, __name__,
                                   static_folder="static",
                                   template_folder="templates",
                                   static_url_path=f"/{PACKAGE_NAME}/static")

        self.blueprint.add_url_rule("/object", "object", self.show_object)
        # self.blueprint.add_url_rule("/", "home", self.show_home)
        self.blueprint.add_url_rule("/about", "about", self.show_about)

        for reg in self.objects:
            if isinstance(reg, RegisterOfRegisters):

            self.blueprint.add_url_rule(os.path.join("/", reg.path, "<id>"), reg.path, self.show_register_object)
            
        # self.blueprint.add_url_rule(os.path.join("/",reg.path), "home", self.show_home)
        # self.blueprint.add_url_rule(os.path.join("/",reg.path), self.rofr.get_reg_endpoint(), self.show_rofr)

        app.register_blueprint(self.blueprint)

    def show_home(self):
        # Need to check headers, as this could be showing the reg-of-reg etc
        return render_template(DEFAULT_TEMPLATE_HOME)

    def show_about(self):
        return render_template(DEFAULT_TEMPLATE_ABOUT)

    def show_register_object(self, id):        
        reg_path = request.endpoint.split(".", 1)[1]
        register = self.register_for_path(reg_path)

        view_key = request.args.get('_view')
        format_key = request.args.get('_format')

        view = register.get_view(view_key) if view_key else register.get_default_view()
        if view == None:
            raise NotImplementedError("No view exists of type '{}' on the requested object".format(view_key))

        format = view.get_format(format_key) if format_key else view.get_default_format()
        if format == None:
            raise NotImplementedError("No format exists of type '{}' on the requested view".format(format_key))

        uri = register.get_uri_for(id)

        return format.render_response(uri, view, register, request)

    def show_rofr(self, id):        
        reg_path = request.endpoint.split(".", 1)[1]
        register = self.register_for_path(reg_path)

        view, format = self.get_view_format(request, register)

        uri = register.get_uri_for(id)

        return format.render_response(uri, view, register, request)

    # this function is here to allow linkdata.gov.au redirect to be cleaner
    def show_object(self):
        uri = request.args.get('uri', type=str, default=None)        

        obj = self.object_for_uri(uri)
        if obj:
            view, format = self.get_view_format(request, obj)
            return format.render_response(uri, view, obj, request)

        reg = self.register_for_uri(uri)
        if reg:

            return 

        # if register != None:
        #     # redirect to the clean url
        #     url_for(".")
        #     pass
        # else:
        #     pass
        #     # show an error

    def object_for_uri(self, uri):
        obj = next((obj for obj in self.objects if obj.uri == uri), None)
        if obj:
            return obj
        

    def register_for_uri(self, uri):
        return next((obj for obj in self.objects if isinstance(obj, Register) and uri in obj), None)

    def register_for_path(self, path):
        return next((reg for reg in self.objects if reg.path == path), None)

    def get_view_format(self, request, obj):
        view_key = request.args.get('_view')
        format_key = request.args.get('_format')

        view = obj.get_view(view_key) if view_key else obj.get_default_view()
        if view == None:
            raise NotImplementedError("No view exists of type '{}' on the requested object".format(view_key))

        format = view.get_format(format_key) if format_key else view.get_default_format()
        if format == None:
            raise NotImplementedError("No format exists of type '{}' on the requested view".format(format_key))

        return (view, format)
