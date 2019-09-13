from urlparse import urljoin


class ObjectGroup: 
    def __init__(base_uri):
        self.base_uri = base_uri # check all lowercase and valid
        self.creators = []

    def add_creators(*creators):        
        for c in creators:
            self.add_creator(c)

    def add_creator(creator):        
        creator.set_group(self)
        self.creators.append(creator)        

    def creator_for_uri(uri):  
        base, objectId = uri.rsplit('/', 1)      
        return next( c for c in self.creator if c.get_base_uri() == base, None)
