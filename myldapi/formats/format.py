from flask import make_response
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
        raise NotImplementedError('Must implement the render_content method')

    def render_response(self, uri, view, lang, parent_register, **kwargs):
        content = self.render_content(uri, view, lang, parent_register, **kwargs)
        headers = {
            'Content-Type': self.default_media_type(),
            'Profile': f"<{view.profile_uri}>",
            # 'Language': lang #set the language eventually
        }
        return make_response(content, headers)
