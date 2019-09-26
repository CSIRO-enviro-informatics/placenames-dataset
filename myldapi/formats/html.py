from .format import Format
from flask import request, Response, render_template
from ..utils import id_from_uri, base_from_uri, find_prop
from flask_paginate import Pagination

class HTMLFormat(Format):
    def __init__(self, template):
        super().__init__("HTML Formatter", 
                         "Provides a human readable HTML page.",
                         "text/html",
                         "html")
        self.template = template

    def render_response(self, uri, view, parent_register, request, **kwargs):
        props = view.get_attributes(uri, **kwargs)        

        html_vars = {
            "uri": uri,
            "id": id_from_uri(uri),
            "base_uri": base_from_uri(uri),
            "type_uri": parent_register.type_uri,
            "type_name": parent_register.type_name,
            "view": view,
            "parent_register": parent_register,
            "attr_map": props,
            "find_prop": find_prop
        }
        html_vars.update(kwargs)

        item_count = next((v.value for am, v in props if am.varname == "item_count"), None)        
        if "page" in html_vars and "per_page" in html_vars and item_count:
            html_vars["pagination"] = Pagination(page=html_vars['page'], 
                                                 per_page=html_vars['per_page'], 
                                                 total=item_count, 
                                                 css_framework="bootstrap4")

        return Response(render_template(self.template, **html_vars), mimetype=self.default_media_type())

