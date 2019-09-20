import os
from .utils import id_from_uri, base_from_uri
from .register import Register
from .views import AlternatesView, RegisterView


class RegisterOfRegisters(Register):
    def __init__(self, base_uri, registers, name="Register of Registers", path="", views=None):
        if views == None:
            views = [
                RegisterView(registers)
            ]

        self.registers = registers

        super().__init__(name=name,
                         path=path,
                         base_uri=base_uri,
                         type_uri="http://purl.org/linked-data/registry#Register",
                         views=views
                         )

    def get_label_for(id):
        return str(id)

    def list_uris(self, page=0, per_page=20):
        reg_uris = [r.base_uri for r in self.registers]
        return reg_uris[page*per_page:(page*per_page)+per_page]

    def get_count(self):
        return len(self.registers)

    def get_view(self, key):
        return next((v for v in self.views if v.key == key), None)
