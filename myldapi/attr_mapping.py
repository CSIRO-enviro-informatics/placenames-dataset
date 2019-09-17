class AttributeMapping:
    def __init__(self, varname, typefunc=str, predicates=None, **kwargs):
        self.__dict__.update(kwargs)
        self.varname = varname
        self.predicates = predicates
        self.typefunc = typefunc

        if predicates != None and not isinstance(predicates, list):
            self.predicates = [predicates]
