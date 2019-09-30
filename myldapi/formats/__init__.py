from .rdf_formats import TurtleFormat, RDFXMLFormat, JSONLDFormat, NTFormat, N3Format
from .format import Format
from .html import HTMLFormat
from .rdf_base import RDFBaseFormat
from .json import JSONFormat

common_rdf_formats = [JSONFormat(),TurtleFormat(), RDFXMLFormat(), JSONLDFormat(), NTFormat(), N3Format()]