from myldapi.views import SourceView
from myldapi.formats import HTMLFormat, common_rdf_formats
from myldapi.utils import DEFAULT_TEMPLATE_OBJECT
from myldapi.sources import Source


class ASGSView(SourceView):
    def __init__(self, source, template=None):
        if template == None:
            template = DEFAULT_TEMPLATE_OBJECT

        super().__init__(name="ASGS",
                         key="asgs",
                         comment="Basic properties conforming to the ABS ASGS Ontologoy",
                         source=source,
                         formats=[
                              HTMLFormat(template),
                              *common_rdf_formats
                         ])


