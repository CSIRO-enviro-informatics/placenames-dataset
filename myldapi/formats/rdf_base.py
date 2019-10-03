from .format import Format
from flask import request, Response, render_template


class RDFBaseFormat(Format):
    def __init__(self, label, comment, media_types, rdflib_format, extensions=[]):
        super().__init__(label, comment, media_types, extensions=extensions)
        self.rdflib_format = rdflib_format

    def render_content(self, uri, view, lang, parent_register, request, **kwargs):
        graph = view.get_graph(uri, **kwargs)
        response_text = graph.serialize(format=self.rdflib_format, encoding='utf-8')

        #clean up a memory leak from RDFLib
        graph.store.remove((None, None, None))
        graph.destroy({})
        del graph

        return response_text
