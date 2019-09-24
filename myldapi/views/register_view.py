import rdflib
from .view import View
from ..formats import HTMLFormat, common_rdf_formats
from ..utils import DEFAULT_TEMPLATE_REGISTER, DEFAULT_PAGE_SIZE
from ..register import Register
from ..attr_mapping import AttributeMapping, AttributeMappingPredicate as Pred, AttributeMappingValue


class RegisterView(View):
    def __init__(self, register, template=None):
        if template == None:
            template = DEFAULT_TEMPLATE_REGISTER

        super().__init__(name="Registry Ontology",
                         comment="A simple list-of-items view taken from the Registry Ontology",
                         key="reg",
                         formats=[
                             HTMLFormat(template),
                             *common_rdf_formats
                         ])        
        self.register = register

    def get_attributes(self, uri, **kwargs):
        page, per_page = self.get_page_args(**kwargs)
        
        page_uris = self.register.get_item_uris(page, per_page)

        list_mapping = AttributeMapping("uris", f"List of {register.name}", typefunc=list)
        values = [AttributeMappingValue(uri, register.get_label_for(uri), uri) for uri in page_uris]
        
        list_mapping_value = AttributeMappingValue(values, None)

        return [(list_mapping, list_mapping_value)]

    def get_graph(self, uri, **kwargs):
        """return a RDFLIB graph of the object"""
        page, per_page = self.get_page_args(**kwargs)

        raise NotImplementedError('Must implement the get_graph method')

    def get_page_args(self, **kwargs):
        page = kwargs['page'] if 'page' in kwargs else 0
        per_page = kwargs['per_page'] if 'per_page' in kwargs else DEFAULT_PAGE_SIZE
        return page, per_page
