import rdflib
from .view import View
from ..formats import HTMLFormat, common_rdf_formats
from ..utils import DEFAULT_TEMPLATE_ALTERNATES
from ..attr_mapping import AttributeMapping, AttributeMappingPredicate as Pred, AttributeMappingValue

class AlternatesView(View):
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
    
    def get_attributes(self, uri, **kwargs):
        result = []                

        # list_mapping = AttributeMapping("views", f"Views for {self.register.type_name}", typefunc=list)
        # list_mapping_value = AttributeMappingValue(self.register.views, None)
        # result.append((list_mapping, list_mapping_value))

        result.append((AttributeMapping("register", None),
                       AttributeMappingValue(self.register, None)))

        return result
        
    def get_graph(self, uri, **kwargs):
        """return a RDFLIB graph of the object"""
        raise NotImplementedError('Must implement the get_graph method')