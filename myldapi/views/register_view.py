import rdflib
import urllib
import math
from rdflib import URIRef, Literal
from .view import View
from ..formats import HTMLFormat, common_rdf_formats
from ..utils import DEFAULT_TEMPLATE_REGISTER, DEFAULT_PAGE_SIZE, id_from_uri, base_from_uri, bind_common, RDF_a, RDFS
from ..attr_mapping import AttributeMapping, AttributeMappingPredicate as Pred, AttributeMappingValue
import myldapi.rofr

REG = rdflib.Namespace('http://purl.org/linked-data/registry#')
LDP = rdflib.Namespace('http://www.w3.org/ns/ldp#')
XHV = rdflib.Namespace('https://www.w3.org/1999/xhtml/vocab#')

class RegisterView(View):
    def __init__(self, reg_of_regs, template=None):
        if template == None:
            template = DEFAULT_TEMPLATE_REGISTER

        super().__init__(name="Registry Ontology",
                         comment="A simple list-of-items view taken from the Registry Ontology",
                         key="reg",
                         formats=[
                             HTMLFormat(template),
                             *common_rdf_formats
                         ], 
                         profile_uri="http://purl.org/linked-data/registry")
        self.reg_of_regs = reg_of_regs

    def get_attributes(self, uri, **kwargs):
        result = []
        page, per_page = self.get_page_args(**kwargs)

        register = self.get_reg_for_uri(uri)

        child_uris = register.list_uris(page, per_page)

        list_mapping = AttributeMapping("uris", f"List of {register.type_name}", typefunc=list)
        values = [AttributeMappingValue(uri, register.get_label_for(id_from_uri(uri)), uri) for uri in child_uris]

        list_mapping_value = AttributeMappingValue(values, None)

        result.append((list_mapping, list_mapping_value))
        result.append((AttributeMapping("contained_item_class", Pred(REG.containedItemClass)),
                       AttributeMappingValue(register.type_uri, register.type_name, register.type_uri)))

        item_count = register.get_count()
        result.append((AttributeMapping("item_count", None),
                       AttributeMappingValue(item_count, str(item_count))))
        result.append((AttributeMapping("endpoint", None),
                       AttributeMappingValue(register.get_route_endpoint(), register.get_route_endpoint())))
        return result

    def get_graph(self, uri, **kwargs):
        """return a RDFLIB graph of the object"""
        g = rdflib.Graph()
        bind_common(g)

        id = id_from_uri(uri)

        g.bind('reg', REG)
        g.bind('ldp', LDP)
        g.bind('xhv', XHV)

        register = self.get_reg_for_uri(uri)
        g.add((URIRef(uri), RDF_a, REG.Register))
        g.add((URIRef(uri), RDFS.label, Literal(register.name)))
        g.add((URIRef(uri), REG.containedItemClass, URIRef(register.type_uri)))
        if not isinstance(register, myldapi.rofr.RegisterOfRegisters):
            g.add((URIRef(uri), REG.register, URIRef(self.reg_of_regs.get_uri())))

        page, per_page = self.get_page_args(**kwargs)
        child_uris = register.list_uris(page, per_page)

        for child_uri in child_uris:
            g.add((URIRef(child_uri), RDF_a, URIRef(register.type_uri)))
            g.add((URIRef(child_uri), RDFS.label, Literal(register.get_label_for(id_from_uri(child_uri)))))
            g.add((URIRef(child_uri), REG.register, URIRef(register.get_uri())))

            # not really needed, but here because ASGS had it.
            if isinstance(register, myldapi.rofr.RegisterOfRegisters):
                child_reg = next((reg for reg in register.registers if reg.get_uri() == child_uri), None)
                g.add((URIRef(child_uri), REG.containedItemClass, URIRef(child_reg.type_uri)))

        #I think this should contain the the view and format info, it would mean we needed to 
        #pass the request obj in to this method and 'add/update' the page per_page params        
        page_info = URIRef(urllib.parse.urljoin(uri, f"?page={page}&per_page={per_page}"))
        g.add((page_info, RDF_a, LDP.Page))
        g.add((page_info, LDP.pageOf, URIRef(register.get_uri())))
        g.add((page_info, XHV.first, URIRef(urllib.parse.urljoin(uri, f"?page={1}&per_page={per_page}"))))
        g.add((page_info, XHV.next, URIRef(urllib.parse.urljoin(uri, f"?page={page+1}&per_page={per_page}"))))
        last_page = math.ceil(register.get_count() / per_page)
        g.add((page_info, XHV.last, URIRef(urllib.parse.urljoin(uri, f"?page={last_page}&per_page={per_page}"))))
        
        return g


    def get_page_args(self, **kwargs):
        page = kwargs['page'] if 'page' in kwargs else 1
        per_page = kwargs['per_page'] if 'per_page' in kwargs else DEFAULT_PAGE_SIZE
        return page, per_page

    def get_reg_for_uri(self, uri):
        return next((reg for reg in self.reg_of_regs.registers if reg.get_uri() == uri), None)
