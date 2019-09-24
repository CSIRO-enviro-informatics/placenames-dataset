import os
from .utils import id_from_uri, base_from_uri
from .registers import Register
from .views import AlternatesView, RegisterView


class RegisterOfRegisters(Register):
    def __init__(self, uri, registers, name="Register of Registers", path="", views=None):
        if views == None:
            views = [
                RegisterView(registers)
            ]

        self.name = name
        self.registers = registers
        uris = [reg.uri for reg in self.registers]

        super().__init__(uri=uri, 
                         views=views, 
                         item_type="http://purl.org/linked-data/registry#Register", 
                         path=path, 
                         uri_list=uris):

    def get_label(self):
        return self.name

    def get_object(self, uri):
        return next(([reg for reg in self.registers if reg.uri == uri]), None)
