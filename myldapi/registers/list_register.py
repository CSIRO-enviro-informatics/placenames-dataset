import os
from ..utils import id_from_uri, base_from_uri
from ..object import Object
from abc import ABC, abstractmethod

class ListRegister(Object):
    def __init__(self, uri, views, item_type, path, uri_list):
        super().__init__(uri=uri, 
                         type_uri="http://purl.org/linked-data/registry#Register", 
                         views=views,
                         path=path):
        self.item_type = item_type
        self.uri_list = uri_list

    def get_item_uris(self, page=0, per_page=20):
        start = page * per_page
        end = start + per_page
        return uri_list[start:end]

    def get_label(self):
        return f"Register of {item_type}"

    def get_count(self):
        return len(self.uri_list)

    def contains(self, uri):
        return uri in self.uri_list

    @abstractmethod
    def get_object(self, uri):
        pass