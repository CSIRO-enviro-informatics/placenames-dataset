import rdflib
from .view import View
from ..formats import HTMLFormat, common_rdf_formats
from ..utils import DEFAULT_TEMPLATES

class AlternatesView:
    def __init__(self, register, template=None):
        if template == None:
            template = DEFAULT_TEMPLATES.alternates

        super().__init__(name="Alternates View", 
                         comment="The view that lists all other views",
                         namespace="https://promsns.org/def/alt",
                         formats=[
                             HTMLFormat(template),
                             *common_rdf_formats
                         ])                        
        self.register = register
    
    def get_attributes(self, uri):
        """return a dictionary of object attributes"""
        raise NotImplementedError('Must implement the get_attributes method')

    def get_graph(self, uri):
        """return a RDFLIB graph of the object"""
        raise NotImplementedError('Must implement the get_graph method')