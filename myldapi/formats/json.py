from .format import Format
from flask import request, Response, render_template
from decimal import Decimal
import json

class JSONFormat(Format):
    def __init__(self):
        super().__init__("JSON Formatter", 
                         "A JSON payload of the object attributes.",
                         "application/json",
                         "json")

    def render_response(self, uri, view, register, request, **kwargs):
        attr_map = view.get_attributes(uri)
        deets = {}

        # Just the values
        for am, v in attr_map:
            if v.uri:
                val = v.uri
            if v.value:
                val = v.value

            if isinstance(val, Decimal):
                val = float(val)

            deets[am.varname] = val

        # All the details
        # for am, v in attr_map:
        #     obj = {}
        #     if v.uri:
        #         obj["uri"] = v.uri
        #     if v.label:
        #         obj["label"] = v.label
        #     if v.value:
        #         obj["value"] = v.value

        #     if isinstance(v.value, Decimal):
        #         obj["value"] = float(v.value)

        #     deets[am.varname] = obj


        return Response(json.dumps(deets, indent=4), mimetype=self.default_media_type())

