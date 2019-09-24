from abc import ABC, abstractmethod

class Object(ABC): 
    def __init__(self, uri, type_uri, views, path):
        self.uri = uri
        self.type_uri = type_uri
        self.views = views
        self.path = path

        if not isinstance(views, list):
            self.views = [views]

    @abstractmethod
    def get_label(self):
        pass

    def get_view(self, key):
        return next((v for v in self.views if v.key == key), None)

    def get_default_view(self):
        return self.views[0]

    def get_graph_for(self, view=None):
        # return an RDF graph representing the full object, which will be filtered by a Profile
        objectId = id_from_uri(uri)
        return self.get_graph_for_id(objectId)

    def get_graph_for_id(self, id, view=None):
        if view == None:
            view = self.get_default_view()
        return view.get_graph()
