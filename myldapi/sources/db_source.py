import requests
from lxml import etree
from functools import lru_cache
from .source import Source


class DBSource(Source):
    def __init__(self, connection, sql):
        """Init database parameter for the given object"""
        raise NotImplementedError('Must implement the __init__ method')

    @abstractmethod
    def get_object_details(self, uri):
        """return a list of (AttributeMapping, value) tuples populated with their values"""
        pass

    @abstractmethod
    def get_count():
        """The count of total objects in this source"""
        pass

    @abstractmethod
    def get_ids(self, page, per_page):
        """Get a list of ids from the source"""
        pass
