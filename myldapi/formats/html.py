from .format import Format
from flask import request, Response, render_template
from ..utils import id_from_uri, base_from_uri
from flask_paginate import Pagination

class HTMLFormat(Format):
    def __init__(self, template):
        super().__init__("HTML Formatter", 
                         "Provides a human readable HTML page.",
                         "text/html",
                         "html")
        self.template = template

    def render_response(self, uri, view, register, request, **kwargs):
        props = view.get_attributes(uri, **kwargs)        
        html_vars = {
            "uri": uri,
            "id": id_from_uri(uri),
            "base_uri": base_from_uri(uri),
            "type_uri": register.type_uri,
            "type_name": register.name,
            "view": view,
            "register": register,
            "attr_map": props
        }
        
        html_vars.update(kwargs)

        if "page" in html_vars and "per_page" in html_vars:
            html_vars["pagination"] = Pagination(page=page, per_page=per_page, total=register.get_count(), css_framework="bootstrap4")

        return Response(render_template(self.template, **html_vars, **kwargs), mimetype=self.default_media_type())

