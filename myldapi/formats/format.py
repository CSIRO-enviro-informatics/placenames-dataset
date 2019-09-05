# -*- coding: utf-8 -*-
class Format:
    def __init__(
            self,
            label,
            comment,
            mediaType,
    ):
        self.label = label
        self.comment = comment
        self.mediaType = mediaType

    def render(g, req):
        #return a flask repsonse 
        pass
