import rdflib
from .view import View
from ..formats import HTMLFormat, common_rdf_formats
from ..utils import DEFAULT_TEMPLATE_ALTERNATES

class AlternatesView:
    def __init__(self, register, template=None):
        if template == None:
            template = DEFAULT_TEMPLATE_ALTERNATES

        super().__init__(name="Alternates View", 
                         comment="The view that lists all other views",
                         key="alternates",
                         formats=[
                             HTMLFormat(template),
                             *common_rdf_formats
                         ])                        
        self.register = register
    
    def get_attributes(self, uri):
        attr_pairings = []

        return attr_pairings
        
    def get_graph(self, uri):
        """return a RDFLIB graph of the object"""
        raise NotImplementedError('Must implement the get_graph method')