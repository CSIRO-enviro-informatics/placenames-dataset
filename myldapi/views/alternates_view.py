import rdflib
from rdflib import URIRef, Literal, Namespace, BNode
from .view import View
from ..formats import HTMLFormat, common_rdf_formats
from ..utils import DEFAULT_TEMPLATE_ALTERNATES, bind_common, RDF_a, RDFS, XSD
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
        g = rdflib.Graph()
        bind_common(g)

        ALT = Namespace('http://promsns.org/def/alt#')
        g.bind('alt', ALT)
        DCT = Namespace('http://purl.org/dc/terms/')
        g.bind('dct', DCT)
        PROF = Namespace('https://w3c.github.io/dxwg/profiledesc#')
        g.bind('prof', PROF)

        for v in self.register.views:
            v_node = BNode()
            g.add((v_node, RDF_a, ALT.View))
            g.add((v_node, PROF.token, Literal(v.key, datatype=XSD.token)))
            g.add((v_node, RDFS.label, Literal(v.name, datatype=XSD.string)))
            g.add((v_node, RDFS.comment, Literal(v.comment, datatype=XSD.string)))
            g.add((v_node, ALT.hasDefaultFormat, Literal(v.get_default_format().default_media_type(), datatype=XSD.string)))

            if v.namespace is not None:
                g.add((v_node, DCT.conformsTo, URIRef(v.namespace)))

            for f in v.formats:
                g.add((v_node, URIRef(DCT.term('format')), URIRef('http://w3id.org/mediatype/' + f.default_media_type())))

            g.add((URIRef(uri), ALT.view, v_node))

            if v == self.register.get_default_view():
                g.add((URIRef(uri), ALT.hasDefaultView, v_node))
            
        return g