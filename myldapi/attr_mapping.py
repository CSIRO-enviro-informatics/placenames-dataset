from inspect import isclass
from rdflib import URIRef, BNode, Literal
from rdflib.term import Identifier
from .utils import find_prop
class AttributeMapping:
    def __init__(self, varname, label=None, typefunc=None, converter=None, units=None, predicate=None, child_attrs=None, **kwargs):
        self.__dict__.update(kwargs)
        self.varname = varname
        self.label = label
        self.predicate = predicate
        self.typefunc = typefunc
        self.converter = converter
        self.units = units
        self.child_attrs = child_attrs

    def create_value(self, val):        
        typed_val = self.typefunc(val) if self.typefunc else val
        if self.converter:
            return self.converter(typed_val)
        else:
            return AttributeMappingValue(typed_val, None)

    @staticmethod
    def reg_id_converter(register_cls, *args, **kwargs):
        def converter(value):
            id = value
            reg = register_cls(*args, **kwargs)
            uri = reg.get_uri_for(id)
            label = reg.get_label_for(id)
            return AttributeMappingValue(value, label, uri)

        return converter

    @staticmethod
    def base_uri_converter(base_uri):
        def converter(value):
            id = value
            uri = base_uri + id
            return AttributeMappingValue(value, label, uri)

        return converter

    @staticmethod
    def format_converter(template):
        """Takes a string template and applies the value to it"""
        def converter(value):
            formatted = template.format(value)
            return AttributeMappingValue(value, formatted)
        return converter

    @staticmethod
    def basic_converter(func):
        """Applies a function to the value and returns it"""
        def converter(value):
            new_val = func(value)
            return AttributeMappingValue(new_val, None)
        return converter

class AttributeMappingValue:
    def __init__(self, value, label, uri=None):
        self.value = value
        self.label = label
        self.uri = uri
        if not self.uri and isinstance(self.value, str) and self.value.startswith("http"):
            self.uri = self.value

class AttributeMappingPredicate:
    def __init__(self, uri, inverse=False, comment=None, builder=None):
        self.pred_uri = uri
        self.inverse = inverse
        self.comment = comment
        self.builder = builder

    def add_to_graph(self, g, obj_uri, rdf_term_val, attr_map_vals):        
        if self.builder:
            self.builder(g, obj_uri, self, rdf_term_val, attr_map_vals)
        else:
            if not isinstance(obj_uri, Identifier):
                obj_uri = URIRef(obj_uri)

            if self.inverse:
                g.add((rdf_term_val, URIRef(self.pred_uri), obj_uri))
            else:
                g.add((obj_uri, URIRef(self.pred_uri), rdf_term_val))


    @staticmethod
    def node_builder(uri, prop_map):
        """uri can be None, prop_name, or uri"""
        """prop_map is a list of tuples (AttributeMappingPredicate, varname/URIRef/BNode/Literal, optional literal datatype)"""
        def builder(g, obj_uri, pred, rdf_term_val, attr_map_vals):
            if not uri:
                node = BNode()
            elif isinstance(uri, URIRef):
                pass
            elif uri.startswith("http"):
                node = URIRef(uri)
            else: #property mapping
                am, v = find_prop(attr_map_vals, uri)
                if not v.uri:
                    raise ValueError(f"URI lookup via property named {uri} failed")                
                node = URIRef(v.uri)
            
            for prop_pred, uri_or_varname, *extras in prop_map:
                if isinstance(uri_or_varname, Identifier):
                    prop_pred.add_to_graph(g, node, uri_or_varname, attr_map_vals)
                else: # lookup the value
                    am, v = find_prop(attr_map_vals, uri_or_varname)
                    lit = Literal(v.value, datatype=extras[0]) if len(extras) == 1 else Literal(v.value)
                    subject = URIRef(v.uri) if v.uri else lit
                    prop_pred.add_to_graph(g, node, subject, attr_map_vals)

            if pred.inverse:
                g.add((node, URIRef(pred.pred_uri), URIRef(obj_uri)))
            else:
                g.add((URIRef(obj_uri), URIRef(pred.pred_uri), node))

        return builder
    
