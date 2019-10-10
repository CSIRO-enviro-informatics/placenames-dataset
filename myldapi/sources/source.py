from functools import lru_cache

class Source():

    @lru_cache(maxsize=32)
    def get_object_details(self, id):
        """return a list of (AttributeMapping, value) tuples populated with their values"""
        _, attr_pairings = self.get_many_object_details([id])[0]
        return attr_pairings

    def get_count():
        """The count of total objects in this source"""
        raise NotImplementedError('Must implement the get_count method')

    def get_ids(self, startindex, take_count):
        """Get a list of ids from the source"""
        raise NotImplementedError('Must implement the get_ids method')

    def get_many_object_details(self, uri_list):
        """Get a list of ids from the source"""
        raise NotImplementedError('Must implement the get_ids method')


