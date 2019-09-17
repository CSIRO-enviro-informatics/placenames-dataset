import rdflib
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD

GEO = Namespace("http://www.opengis.net/ont/geosparql#")
GEOX = Namespace("http://linked.data.gov.au/def/geox#")
GML = Namespace("http://www.opengis.net/ont/gml#")
OGC = Namespace("http://www.opengis.net/")
ASGS = Namespace('http://linked.data.gov.au/def/asgs#')
DATA = Namespace("http://linked.data.gov.au/def/datatype/")
CRS_OGC = Namespace("http://www.opengis.net/def/crs/OGC/1.3/")
CRS_EPSG = Namespace("http://www.opengis.net/def/crs/EPSG/0/")
QB4ST = Namespace("http://www.w3.org/ns/qb4st/")

PACKAGE_NAME = "myldapi"

DEFAULT_TEMPLATES = {
    "alternates": "{}/alternates.html".format(PACKAGE_NAME),
    "home": "{}/home.html".format(PACKAGE_NAME),
    "object": "{}/object.html".format(PACKAGE_NAME),
    "register": "{}/register.html".format(PACKAGE_NAME),
    "rofr": "{}/registers.html".format(PACKAGE_NAME)
}


def id_from_uri(uri):
    base, objectId = uri.rsplit('/', 1)
    return objectId


def base_from_uri(uri):
    base, objectId = uri.rsplit('/', 1)
    return base
