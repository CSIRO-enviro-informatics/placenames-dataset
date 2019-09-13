import os

class Register: 
    def __init__(self, name, path, base_uri, type_uri):
        self.name = name 
        self.path = path # check all lowercase and valid
        self.base_uri = base_uri # check all lowercase and valid
        self.type_uri = type_uri

    def get_graph_for(self, uri):        
        #return an RDF graph representing the full object, which will be filtered by a Profile
        pass

    def create_list(self, uri, page, page_size):
        return []
    
    def get_uri_for(self, id):
        return os.path.join(self.get_base_uri, id)
    
    def set_group(self, group):
        self.group = group 
