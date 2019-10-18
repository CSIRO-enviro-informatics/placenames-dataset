import requests
from lxml import etree
from functools import lru_cache
from .source import Source
from io import StringIO, BytesIO
from ..utils import id_from_uri
from ..attr_mapping import AttributeMapping


class JSONSource(Source):
    # Mearly a placeholder for this concept
    pass