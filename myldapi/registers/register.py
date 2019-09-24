import os
from ..utils import id_from_uri, base_from_uri
from ..object import Object
from abc import ABC, abstractmethod
from ..views import RegisterView

class Register(Object):
    def __init__(self, uri, item_type, path):
        super().__init__(uri=uri, 
                         type_uri="http://purl.org/linked-data/registry#Register", 
                         views=[
                             RegisterView()
                         ],
                         path=path):
        self.item_type = item_type

    @abstractmethod
    def get_item_uris(self, page=0, per_page=20):
        pass

    def get_label(self):
        return f"Register of {item_type}"

    @abstractmethod
    def get_count(self):
        pass

    @abstractmethod
    def get_object(self, uri):
        pass