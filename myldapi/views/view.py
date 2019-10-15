import rdflib

class View:
    def __init__(self, name, comment, key, formats, profile_uri, languages=['en']):
        self.name = name
        self.comment = comment
        self.key = key
        self.formats = formats
        self.profile_uri = profile_uri
        self.languages = languages

        if not isinstance(formats, list):
            self.formats = [formats]
    
    def get_attributes(self, uri, parent_register, **kwargs):
        """return a dictionary of object attributes"""
        raise NotImplementedError('Must implement the get_attributes method')

    def get_graph(self, uri, parent_register, **kwargs):
        """return a RDFLIB graph of the object"""
        raise NotImplementedError('Must implement the get_graph method')

    def get_default_format(self):
        return self.formats[0]
    
    def get_format(self, media_type):
        priority = next((f for f in self.formats if media_type == f.default_media_type()), None)
        return priority if priority else next((f for f in self.formats if media_type in f.media_types), None)

    def get_format_by_extension(self, ext):
        return next((f for f in self.formats if ext in f.extensions), None)

    def get_default_language(self):
        return self.languages[0]

    def get_many_attributes(self, uri_list, parent_register, **kwargs):
        return [(uri, self.get_attributes(uri, parent_register, **kwargs)) for uri in uri_list]

    def get_many_graphs(self, uri_list, parent_register,  **kwargs):
        return [(uri, self.get_graph(uri, parent_register, **kwargs)) for uri in uri_list]
