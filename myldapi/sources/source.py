
class Source():

    def get_object_details(self, uri):
        """return a list of (AttributeMapping, value) tuples populated with their values"""
        raise NotImplementedError('Must implement the get_object_details method')

    def get_count():
        """The count of total objects in this source"""
        raise NotImplementedError('Must implement the get_count method')

