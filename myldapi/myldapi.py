from flask import current_app, _app_ctx_stack, Blueprint, request, redirect, url_for, Response, render_template


class MyLDApi(object):
    def __init__(self, app=None, registers=[]):
        self.app = app
        self.registers = registers
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('APP_TITLE', 'LDAPI Instance')

        #create a blueprint and attach it to the app?
        self.blueprint = Blueprint("myldapi", __name__, 
            static_folder="static",
            template_folder="templates")

        self.blueprint.add_url_rule("/object", "object", self.show_object)
        self.blueprint.add_url_rule("/", "home", self.show_home)

        app.register_blueprint(self.blueprint)

    def show_home(self):
        # Need to check headers, as this could be showing the reg-of-reg etc
        return render_template("myldapi/home.html")

    #this function is here to allow linkdata.gov.au redirect to be cleaner
    def show_object(self):
        uri = request.args.get('uri', type=str, default=None)        
        creator = next((group for group in self.groups if group.creator_for_uri(uri) != None), None)
        if creator != None:
            #redirect to the clean url
            pass
        else:
            pass
            #show an error
