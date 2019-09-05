import rdflib

class View:
    def __init__(name, comment, namespace, construct_sparql):
        self.name = name
        self.comment = comment
        self.namespace = namespace
        self.construct_sparql = construct_sparql
    
    def subgraph(g, uri):
        focus_obj = rdflib.URIRef(uri)
        triples = g.query(self.construct_sparql, initBindings={'object': focus_obj})
