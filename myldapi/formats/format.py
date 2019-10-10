import os
from flask import make_response
from ..utils import id_from_uri
# -*- coding: utf-8 -*-
class Format:
    def __init__(self, label, comment, media_types, extensions=[]):
        self.label = label
        self.comment = comment
        self.media_types = media_types
        self.extensions = extensions

        if not isinstance(self.media_types, list):
            self.media_types = [media_types]

        if not isinstance(self.extensions, list):
            self.extensions = [extensions]

    def default_media_type(self):
        return self.media_types[0]

    def default_extension(self):
        return self.extensions[0]

    def render_content(self, uri, view, lang, parent_register, **kwargs):
        details = self.get_details(uri, view, lang, parent_register, **kwargs)
        return self.render_details_as_text(details, uri, view, lang, parent_register, **kwargs)

    def get_details(self, uri, view, lang, parent_register, **kwargs):
        """Gets the graph, or attributes needed for render"""
        raise NotImplementedError('Must implement the get_details method')

    def render_details_as_text(self, details, uri, view, lang, parent_register, **kwargs):
        raise NotImplementedError('Must implement the render_details_as_text method')

    def render_response(self, uri, view, lang, parent_register, **kwargs):
        content = self.render_content(uri, view, lang, parent_register, **kwargs)
        headers = {
            'Content-Type': self.default_media_type(),
            'Profile': f"<{view.profile_uri}>",
            # 'Language': lang #set the language eventually
        }
        return make_response(content, headers)        

    def export_many(self, output_dir, uri_list, view, lang, parent_register, **kwargs):
        uri_deets = self.get_many_details(uri_list, view, lang, parent_register, **kwargs)
        for uri, details in uri_deets:                                                                                                                                            
            print(f"Exporting: {uri}")            
            content = self.render_details_as_text(details, uri, view, lang, parent_register, **kwargs)
            filename = f"{id_from_uri(uri)}.{self.default_extension()}"
            output_file = os.path.join(output_dir, filename)
            with open(output_file, "w") as f:
                f.write(content)

    def get_many_details(self, uri_list, view, lang, parent_register, **kwargs):
        raise NotImplementedError('Must implement the get_many_details method')
