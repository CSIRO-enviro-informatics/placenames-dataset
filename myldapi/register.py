import os
from .utils import id_from_uri, base_from_uri
from .views import AlternatesView
class Register:
    def __init__(self, name, path, base_uri, type_uri, type_name, views):
        self.name = name
        self.path = path
        self.base_uri = base_uri
        self.type_uri = type_uri
        self.type_name = type_name
        self.views = views

        if not isinstance(views, list):
            self.views = [views]

        #Everyone has an alternates view
        self.views.append(AlternatesView(self)) 

        if self.base_uri[-1] == "/":
            raise ValueError("base_uri must not have trailing '/' ")

    def get_graph_for(self, uri, view=None):
        # return an RDF graph representing the full object, which will be filtered by a Profile
        objectId = id_from_uri(uri)
        return self.get_graph_for_id(objectId)

    def get_graph_for_id(self, id, view=None):
        if view == None:
            view = self.get_default_view()
        return view.get_graph()

    def get_label_for(self, id):
        return f"{self.type_name}# {str(id)}"

    def list_uris(self, page=1, per_page=20):
        raise NotImplementedError('Must implement the get_ids method')

    def can_resolve_uri(self, uri):
        base = base_from_uri(uri)
        return base == self.base_uri

    def get_uri_for(self, id):
        return os.path.join(self.base_uri, id)

    def get_count(self):
        raise NotImplementedError('Must implement the get_count method')

    def get_default_view(self):
        return self.views[0]

    def get_view(self, key):
        return next((v for v in self.views if v.key == key), None)

    def get_route_endpoint(self):
        """Used to provide an endpoint name for the flask blueprint"""        
        return f"{self.path}/register"
