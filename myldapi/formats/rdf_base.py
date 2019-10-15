import io
from .format import Format
from flask import request, Response, render_template


class RDFBaseFormat(Format):
    def __init__(self, label, comment, media_types, rdflib_format, extensions=[]):
        super().__init__(label, comment, media_types, extensions=extensions)
        self.rdflib_format = rdflib_format

    def get_details(self, uri, view, lang, parent_register, **kwargs):
        return view.get_graph(uri, parent_register, **kwargs)        

    def get_many_details(self, uri_list, view, lang, parent_register, **kwargs):
        return view.get_many_graphs(uri_list, parent_register, **kwargs)

    def render_details_as_text(self, details, uri, view, lang, parent_register, **kwargs):
        graph = details

        b_response = graph.serialize(format=self.rdflib_format, encoding='utf-8')
        
        #clean up a memory leak from RDFLib
        graph.store.remove((None, None, None))
        graph.destroy({})
        del graph
        
        return str(b_response, encoding='utf-8')
