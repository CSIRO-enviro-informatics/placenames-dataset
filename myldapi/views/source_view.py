import rdflib
from .view import View

class SourceView(View):
    def __init__(self, name, comment, source):
        super().__init__(name, comment)
        self.source = source
    
    def get_attributes(self, uri):
        base, objectId = uri.rsplit('/', 1)
        attr_mappings = self.source.get

    def get_graph(self, uri):
        base, objectId = uri.rsplit('/', 1)
        self.source.

