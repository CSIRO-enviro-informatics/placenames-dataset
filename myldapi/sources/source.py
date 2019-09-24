from abc import ABC, abstractmethod

class Source(ABC):

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

