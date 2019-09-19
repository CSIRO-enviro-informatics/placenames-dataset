import requests
from lxml import etree
from functools import lru_cache
from .source import Source


class DBSource(Source):
    def __init__(self, connection, sql):
        """Init database parameter for the given object"""
        raise NotImplementedError('Must implement the __init__ method')

    def get_object_details(self, uri):
        """return a list of (AttributeMapping, value) tuples populated with their values"""
        raise NotImplementedError('Must implement the get_object_details method')

    def get_count():
        """The count of total objects in this source"""
        raise NotImplementedError('Must implement the get_count method')

    def get_ids(self, startindex, count):
        """Get a list of ids from the source"""
        raise NotImplementedError('Must implement the get_ids method')
