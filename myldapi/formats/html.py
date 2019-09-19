from .format import Format
from flask import request, Response, render_template
from ..utils import id_from_uri, base_from_uri


class HTMLFormat(Format):
    def __init__(self, template):
        super().__init__("HTML Formatter", 
                         "Provides a human readable HTML page.",
                         "text/html",
                         "html")
        self.template = template

    def render_response(self, uri, view, register, request):
        props = view.get_attributes(uri)
        html_vars = {
            "uri": uri,
            "id": id_from_uri(uri),
            "base_uri": base_from_uri(uri),
            "type_uri": register.type_uri,
            "type_name": register.name,
            "attr_map": props
        }
        return Response(render_template(self.template, **html_vars), mimetype=self.default_media_type())

