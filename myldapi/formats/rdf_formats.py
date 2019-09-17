from .rdf_format import RDFBaseFormat
from flask import request, Response, render_template

class TurtleFormat(RDFBaseFormat):
    def __init__(self):
        super().__init__(label="RDF Turtle Format", 
                         comment="", 
                         media_types=["text/turtle","text/ttl"], 
                         rdflib_format="turtle",
                         extensions=["ttl"])

class N3Format(RDFBaseFormat):
    def __init__(self):
        super().__init__(label="RDF N3 Format", 
                         comment="", 
                         media_types=["text/n3"], 
                         rdflib_format="n3",
                         extensions=["n3"])

class RDFXMLFormat(RDFBaseFormat):
    def __init__(self):
        super().__init__(label="RDF XML Format", 
                         comment="", 
                         media_types=["application/rdf+xml", "application/rdf", "application/rdf xml"], 
                         rdflib_format="turtle",
                         extensions=["xml"])

class JSONLDFormat(RDFBaseFormat):
    def __init__(self):
        super().__init__(label="RDF JSON-LD Format", 
                         comment="", 
                         media_types=["application/ld+json", "application/json", "application/ld json"], 
                         rdflib_format="json-ld",
                         extensions=["jsonld"])

class NTFormat(RDFBaseFormat):
    def __init__(self):
        super().__init__(label="RDF n-triples Format", 
                         comment="", 
                         media_types=["application/n-triples", "text/ntriples", "text/n-triples", "text/plain"], 
                         rdflib_format="nt",
                         extensions=["jsonld"])
