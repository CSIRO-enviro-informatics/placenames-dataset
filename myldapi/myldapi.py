from flask import current_app, _app_ctx_stack, Blueprint, request, redirect, url_for, Response, render_template


class MyLDApi(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        #create a blueprint and attach it to the app?
        blueprint = Blueprint("myldapi", __name__, 
            static_folder="static",
            template_folder="templates")

        blueprint.add_url_rule('/object', 'object', self.show_object)

        app.register_blueprint(blueprint)

    #this function is here to allow linkdata.gov.au redirect to be cleaner
    def show_object():
        uri = request.args.get('uri', type=str, default=None)
        #if we know about this tupe
            #redirect to the clean url
        #else
            #show an error
