import rdflib
from rdflib import URIRef, Literal
from .view import View
from ..utils import id_from_uri, base_from_uri, bind_common, RDF_a


class SourceView(View):
    def __init__(self, name, comment, key, formats, profile_uri, source ):
        super().__init__(name, comment, key, formats, profile_uri)
        self.source = source

    def get_attributes(self, uri, **kwargs):
        return self.source.get_object_details(uri)

    def get_graph(self, uri, **kwargs):
        attr_values = self.source.get_object_details(uri)
        g = rdflib.Graph()
        bind_common(g)

        for am, val in attr_values:
            if am.predicate:
                v = URIRef(val.uri) if val.uri else Literal(val.value)
                am.predicate.add_to_graph(g, uri, v, attr_values)

        return g
