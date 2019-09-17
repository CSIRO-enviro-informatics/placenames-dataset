import rdflib

class View:
    def __init__(self, name, comment, key, namespace, construct_sparql, formats):
        self.name = name
        self.comment = comment
        self.namespace = namespace
        self.construct_sparql = construct_sparql
        self.formats = formats

        if not isinstance(formats, list):
            self.formats = [formats]
    
    def get_attributes(self, uri):
        """return a dictionary of object attributes"""
        raise NotImplementedError('Must implement the get_attributes method')

    def get_graph(self, uri):
        """return a RDFLIB graph of the object"""
        raise NotImplementedError('Must implement the get_graph method')