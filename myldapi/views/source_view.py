import rdflib
import urllib
from rdflib import URIRef, Literal
from .view import View
from ..utils import id_from_uri, base_from_uri, bind_common, RDF_a


class SourceView(View):
    def __init__(self, name, comment, key, formats, profile_uri, source ):
        super().__init__(name, comment, key, formats, profile_uri)
        self.source = source

    def get_attributes(self, uri, parent_register, **kwargs):        
        return self.source.get_object_details(id_from_uri(uri))

    def get_graph(self, uri, parent_register, **kwargs):
        attr_values = self.source.get_object_details(id_from_uri(uri))
        g = self.graph_from_attributes(uri, attr_values)
        g.add((URIRef(uri), RDF_a, URIRef(parent_register.type_uri)))
        return g

    def graph_from_attributes(self, uri, attr_values):
        g = rdflib.Graph()
        bind_common(g)

        for am, val in attr_values:
            if am.predicate and val:
                v = URIRef(val.uri) if val.uri else Literal(val.value)
                am.predicate.add_to_graph(g, uri, v, attr_values)

        return g

    def get_many_attributes(self, uri_list, **kwargs):
        """Override with an optimised batch fetch"""
        # Assuming all uris, have same base, if not, we have a problem. 
        # Could do a lookup to original list by id to fix that, but its slower so I wont yet
        base = base_from_uri(uri_list[0])
        id_list = [id_from_uri(uri) for uri in uri_list]
        id_mappings = self.source.get_many_object_details(id_list)
                
        return [(urllib.parse.urljoin(base, id), details) for id, details in id_mappings]

    def get_many_graphs(self, uri_list, **kwargs):
        """Override with an optimised batch fetch"""
        uri_attr = self.get_many_attributes(uri_list, **kwargs)
        return [(uri, self.graph_from_attributes(uri, attrs)) for uri, attrs in uri_attr]
