import rdflib
from .view import View
from ..utils import id_from_uri, base_from_uri


class SourceView(View):
    def __init__(self, name, comment, key, formats, source):
        super().__init__(name, comment, key, formats)
        self.source = source

    def get_attributes(self, uri, **kwargs):
        return self.source.get_object_details(uri)

    def get_graph(self, uri, **kwargs):
        attr_values = self.source.get_object_details(uri)
        g = rdflib.Graph()
        g.bind('asgs', ASGS)
        g.bind('geo', GEO)
        g.bind('geox', GEOX)
        g.bind('data', DATA)

        for am, val in attr_values:
            for p in am.predicates:    
                pass            

        return g
