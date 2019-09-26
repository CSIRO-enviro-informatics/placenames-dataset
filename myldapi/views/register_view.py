import rdflib
from .view import View
from ..formats import HTMLFormat, common_rdf_formats
from ..utils import DEFAULT_TEMPLATE_REGISTER, DEFAULT_PAGE_SIZE, id_from_uri
from ..attr_mapping import AttributeMapping, AttributeMappingPredicate as Pred, AttributeMappingValue


class RegisterView(View):
    def __init__(self, registers, template=None):
        if template == None:
            template = DEFAULT_TEMPLATE_REGISTER

        super().__init__(name="Registry Ontology",
                         comment="A simple list-of-items view taken from the Registry Ontology",
                         key="reg",
                         formats=[
                             HTMLFormat(template),
                             *common_rdf_formats
                         ])
        self.registers = registers

    def get_attributes(self, uri, **kwargs):
        result = []
        page, per_page = self.get_page_args(**kwargs)

        register = next((reg for reg in self.registers if reg.base_uri == uri), None)

        page_uris = register.list_uris(page, per_page)

        list_mapping = AttributeMapping("uris", f"List of {register.type_name}", typefunc=list)
        values = [AttributeMappingValue(uri, register.get_label_for(id_from_uri(uri)), uri) for uri in page_uris]

        list_mapping_value = AttributeMappingValue(values, None)

        result.append((list_mapping, list_mapping_value))
        result.append((AttributeMapping("contained_item_class", Pred("http://purl.org/linked-data/registry#containedItemClass")),
                       AttributeMappingValue(register.type_uri, register.type_name, register.type_uri)))

        item_count = register.get_count()
        result.append((AttributeMapping("item_count", None),
                       AttributeMappingValue(item_count, str(item_count))))
        result.append((AttributeMapping("endpoint", None),
                       AttributeMappingValue(register.get_route_endpoint(), register.get_route_endpoint())))
        return result

    def get_graph(self, uri, **kwargs):
        """return a RDFLIB graph of the object"""
        page, per_page = self.get_page_args(**kwargs)

        raise NotImplementedError('Must implement the get_graph method')

    def get_page_args(self, **kwargs):
        page = kwargs['page'] if 'page' in kwargs else 1
        per_page = kwargs['per_page'] if 'per_page' in kwargs else DEFAULT_PAGE_SIZE
        return page, per_page
