#Us this class to create graph representing the object type

class ObjectCreator: 
    def __init__(object_type, base_uri):
        self.object_type = object_type
        self.uri = base_uri

    def create_single_graph(uri):        
        #return an RDF graph
        pass

    def create_list(uri, page, page_size):
        return []
        pass