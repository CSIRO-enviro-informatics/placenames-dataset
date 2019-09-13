import rdflib

class Profile:
    def __init__(name, comment, namespace, construct_sparql):
        self.name = name
        self.comment = comment
        self.namespace = namespace
        self.construct_sparql = construct_sparql
    
    def augmented_graph(g, uri):
        """ Converts the objects graph into a new form """
        
        focus_obj = rdflib.URIRef(uri)
        triples = g.query(self.construct_sparql, initBindings={'object': focus_obj})
