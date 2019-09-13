import os


class Register:
    def __init__(self, name, path, base_uri, type_uri):
        self.name = name
        self.path = path
        self.base_uri = base_uri
        self.type_uri = type_uri

        # if self.base_uri[-1] == "/":
        #     raise ValueError("base_uri must not have trailing '/' ")

    def get_graph_for(self, uri):
        # return an RDF graph representing the full object, which will be filtered by a Profile
        base, objectId = uri.rsplit('/', 1)
        return self.get_graph_for_id(objectId)

    def get_graph_for_id(self, id):
        raise NotImplementedError('Must implement the get_graph_for_id method')

    def create_list(self, uri, page, page_size):
        return []

    def can_resolve_uri(self, uri):
        base, objectId = uri.rsplit('/', 1)
        return base == self.base_uri

    def get_uri_for(self, id):
        return os.path.join(self.get_base_uri, id)

    def set_group(self, group):
        self.group = group
