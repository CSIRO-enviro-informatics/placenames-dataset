import rdflib
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD

GEO = Namespace("http://www.opengis.net/ont/geosparql#")
GEOX = Namespace("http://linked.data.gov.au/def/geox#")
GML = Namespace("http://www.opengis.net/ont/gml#")
OGC = Namespace("http://www.opengis.net/")
DATA = Namespace("http://linked.data.gov.au/def/datatype/")
CRS_OGC = Namespace("http://www.opengis.net/def/crs/OGC/1.3/")
CRS_EPSG = Namespace("http://www.opengis.net/def/crs/EPSG/0/")
QB4ST = Namespace("http://www.w3.org/ns/qb4st/")

RDF_a = RDF.term('type')

PACKAGE_NAME = "myldapi"

DEFAULT_TEMPLATE_HOME = "{}/home.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_ABOUT = "{}/about.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_ALTERNATES = "{}/alternates.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_OBJECT = "{}/object.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_REGISTER = "{}/register.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_ROFR = "{}/registers.html".format(PACKAGE_NAME)

DEFAULT_PAGE_SIZE = 20

def id_from_uri(uri):
    base, objectId = uri.rsplit('/', 1)
    return objectId

def base_from_uri(uri):
    base, objectId = uri.rsplit('/', 1)
    return base

def check_config(name, app):
    if not name in app.config:
        raise ValueError(f"{name} must be set in the config pre-initialistaion of {PACKAGE_NAME}")

def find_prop(pairs, varname):
    return next(((am, v) for am, v in pairs if am.varname == varname), None)

def bind_common(graph):
    graph.bind('geo', GEO)
    graph.bind('geox', GEOX)
    graph.bind('data', DATA)
    graph.bind('ogc', OGC)
    graph.bind('gml', GML)
    graph.bind('qb4st', QB4ST)
