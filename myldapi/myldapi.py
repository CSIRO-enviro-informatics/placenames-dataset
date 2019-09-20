from flask import current_app, _app_ctx_stack, Blueprint, request, redirect, url_for, Response, render_template
from .utils import DEFAULT_TEMPLATE_HOME, DEFAULT_TEMPLATE_ABOUT

class MyLDApi(object):
    def __init__(self, app=None, registers=[]):
        self.app = app
        self.registers = registers
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("APP_TITLE", "LDAPI Instance")
        app.config.setdefault("DATASET_NAME", "Unknown")
        app.config.setdefault("CITATION_TEMPLATE", "{type} {id}. {type} from the {dataset}. {uri}")

        self.blueprint = Blueprint("myldapi", __name__,
                                   static_folder="static",
                                   template_folder="templates",
                                   static_url_path="/myldapi/static")

        self.blueprint.add_url_rule("/object", "object", self.show_object)
        self.blueprint.add_url_rule("/", "home", self.show_home)
        self.blueprint.add_url_rule("/about", "about", self.show_about)

        for reg in self.registers:
            self.blueprint.add_url_rule(
                "/{}/<id>".format(reg.path), reg.path, self.show_register)
            self.blueprint.add_url_rule(
                "/{}".format(reg.path), reg.path, self.show_register)

        app.register_blueprint(self.blueprint)

    def show_home(self):
        # Need to check headers, as this could be showing the reg-of-reg etc
        return render_template(DEFAULT_TEMPLATE_HOME)

    def show_about(self):
        return render_template(DEFAULT_TEMPLATE_ABOUT)

    def show_register(self, id=None):        
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

        if id:
            uri = register.get_uri_for(id)
        else:
            raise NotImplementedError("Need to render the register itself")

        return format.render_response(uri, view, register, request)

    # this function is here to allow linkdata.gov.au redirect to be cleaner
    def show_object(self):
        uri = request.args.get('uri', type=str, default=None)
        register = register_for_uri(uri)
        if register != None:
            # redirect to the clean url
            url_for(".")
            pass
        else:
            pass
            # show an error

    def register_for_uri(self, uri):
        return next((reg for reg in self.registers if reg.can_resolve_uri(uri)), None)

    def register_for_path(self, path):
        return next((reg for reg in self.registers if reg.path == path), None)
