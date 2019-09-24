import os
from ..utils import id_from_uri, base_from_uri
from ..object import Object
from abc import ABC, abstractmethod
import inspect

class SourceRegister(Object):
    def __init__(self, uri, item_type, source, base_uri, path):
        super().__init__(uri=uri, 
                         type_uri="http://purl.org/linked-data/registry#Register",
                         path=path):
        self.item_type = item_type
        self.source = source
        self.base_uri = base_uri

        if inspect.isclass(self.item_type)
            self.class_type = self.item_type
            self.item_type = self.get_object("http://fake").type_uri

    def get_item_uris(self, page=0, per_page=20):
        ids = self.source.get_ids(page*per_page, per_page)
        return [self.get_uri_for(id) for id in ids]

    def get_label(self):
        return f"Register of {item_type}"

    def get_count(self):
        return len(self.uri_list)

    def get_uri_for(self, id):
        return os.path.join(self.base_uri, id)

    def get_object(self, uri):
        return self.class_type(uri)
