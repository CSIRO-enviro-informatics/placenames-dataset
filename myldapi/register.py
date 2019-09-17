import os
from .utils import id_from_uri, base_from_uri

class Register:
    def __init__(self, name, path, base_uri, type_uri, views):
        self.name = name
        self.path = path
        self.base_uri = base_uri
        self.type_uri = type_uri
        self.views = views

        if not isinstance(view, list):
            self.views = [views]

        # if self.base_uri[-1] == "/":
        #     raise ValueError("base_uri must not have trailing '/' ")

    def get_graph_for(self, uri, view=None):
        # return an RDF graph representing the full object, which will be filtered by a Profile
        objectId = id_from_uri(uri)
        return self.get_graph_for_id(objectId)

    def get_graph_for_id(self, id, view=None):
        raise NotImplementedError('Must implement the get_graph_for_id method')

    def create_list(self, uri, page, page_size):
        return []

    def can_resolve_uri(self, uri):
        base = base_from_uri(uri)
        return base == self.base_uri

    def get_uri_for(self, id):
        return os.path.join(self.get_base_uri, id)

    def set_group(self, group):
        self.group = group
