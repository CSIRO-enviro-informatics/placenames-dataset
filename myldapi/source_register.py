import os
from .utils import id_from_uri, base_from_uri
from .register import Register

class SourceRegister(Register):
    def __init__(self, name, path, base_uri, type_uri, type_name, views, source):
        super().__init__(name, path, base_uri, type_uri, type_name, views) 
        self.source = source
    
    def list_uris(self, page=1, per_page=20):
        startindex = (page - 1) * per_page
        take = per_page if startindex + per_page < self.get_count() else self.get_count() - startindex 
        ids = self.source.get_ids(startindex, take)
        return [self.get_uri_for(id) for id in ids]

    def get_count(self):
        return self.source.get_count()
