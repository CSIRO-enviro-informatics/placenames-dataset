import .format
from flask import request, Response, render_template
import json

class HTMLFormat(Format):
    def __init__(self):
        super().__init__("JSON Formatter", 
                         "A JSON payload of the object attributes.",
                         "application/json",
                         "json")

    def render_response(self, uri, view, request):
        deets = view.get_attributes(uri)
        return Response(json.dumps(deets, indent=4), mimetype=self.default_media_type())
