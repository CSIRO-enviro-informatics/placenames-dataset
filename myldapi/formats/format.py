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

    def render_response(self, uri, view, register, request):
        raise NotImplementedError('Must implement the render_response method')
