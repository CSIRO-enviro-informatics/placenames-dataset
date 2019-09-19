from inspect import isclass

class AttributeMapping:
    def __init__(self, varname, label=None, typefunc=str, converter=None, units=None, predicate=None, **kwargs):
        self.__dict__.update(kwargs)
        self.varname = varname
        self.label = label
        self.predicate = predicate
        self.typefunc = typefunc
        self.converter = converter
        self.units = units

    def create_value(self, val):        
        typed_val = self.typefunc(val)
        if self.converter:
            return self.converter(typed_val)
        else:
            return AttributeMappingValue(str(typed_val))

    @staticmethod
    def reg_id_converter(register_cls, *args, **kwargs):
        def converter(value):
            id = value
            reg = register_cls(*args, **kwargs)
            uri = reg.get_uri_for(id)
            label = reg.get_label_for(id)
            return AttributeMappingValue(label, uri)

        return converter
            
    @staticmethod
    def format_converter(template):
        def converter(value):
            formatted = template.format(value)
            return AttributeMappingValue(formatted)
        return converter

class AttributeMappingValue:
    def __init__(self, label, uri=None):
        self.label = label
        self.uri = uri

class AttributeMappingPredicate:
    def __init__(self, uri, inverse=False, comment=None, builder=None):
        self.pred_uri = uri
        self.inverse = inverse
        self.comment = comment
        self.builder = builder

    def add_to_graph(self, g, obj_uri, val):        
        if self.builder:
            self.builder(g, obj_uri, val)
        else:
            if self.inverse:
                g.add((val, self.pred_uri, obj_uri))
            else:
                g.add((obj_uri, self.pred_uri, val))

