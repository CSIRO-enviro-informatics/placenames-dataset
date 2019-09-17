import .format
from flask import request, Response, render_template


class HTMLFormat(Format):
    def __init__(self, template):
        super().__init__("HTML Formatter", 
                         "Provides a human readable HTML page.",
                         "text/html",
                         "html")
        self.template = template

    def render_response(self, uri, view, request):
        deets = view.get_attributes(uri)
        return Response(render_template(self.template, *deets), mimetype=self.default_media_type())

