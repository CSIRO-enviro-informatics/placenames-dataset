from flask import current_app, _app_ctx_stack, Blueprint, request, redirect, url_for, Response, render_template


class MyLDApi(object):
    def __init__(self, app=None, registers=[]):
        self.app = app
        self.registers = registers
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('APP_TITLE', 'LDAPI Instance')

        # create a blueprint and attach it to the app?
        self.blueprint = Blueprint("myldapi", __name__,
                                   static_folder="static",
                                   template_folder="templates")

        self.blueprint.add_url_rule("/object", "object", self.show_object)
        self.blueprint.add_url_rule("/", "home", self.show_home)

        for reg in self.registers:
            self.blueprint.add_url_rule(
                "/{}/<id>".format(reg.path), reg.path, self.show_register)
            self.blueprint.add_url_rule(
                "/{}".format(reg.path), reg.path, self.show_register)

        app.register_blueprint(self.blueprint)

    def show_home(self):
        # Need to check headers, as this could be showing the reg-of-reg etc
        return render_template("myldapi/home.html")

    def show_register(self):
        return render_template()

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
