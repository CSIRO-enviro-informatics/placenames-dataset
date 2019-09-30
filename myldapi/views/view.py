import rdflib

class View:
    def __init__(self, name, comment, key, formats):
        self.name = name
        self.comment = comment
        self.key = key
        self.formats = formats

        if not isinstance(formats, list):
            self.formats = [formats]
    
    def get_attributes(self, uri, **kwargs):
        """return a dictionary of object attributes"""
        raise NotImplementedError('Must implement the get_attributes method')

    def get_graph(self, uri, **kwargs):
        """return a RDFLIB graph of the object"""
        raise NotImplementedError('Must implement the get_graph method')

    def get_default_format(self):
        return self.formats[0]
    
    def get_format(self, media_type):
        priority = next((f for f in self.formats if media_type == f.default_media_type()), None)
        return priority if priority else next((f for f in self.formats if media_type in f.media_types), None)

    def get_format_by_extension(self, ext):
        return next((f for f in self.formats if ext in f.extensions), None)
