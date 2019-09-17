from ..myldapi.views import View
from ..myldapi.formats import HTMLFormat, common_rdf_formats
from ..myldapi.utils import DEFAULT_TEMPLATES
from ..myldapi.sources.wfs_source import WFSSource


class ASGSView(SourceView):
    def __init__(self, source, template=None):
        if template == None:
            template = DEFAULT_TEMPLATES.object

        super().__init__(name="ASGS",
                         key="asgs",
                         comment="Basic properties conforming to the ABS ASGS Ontologoy",
                         source=source,
                         formats=[
                              HTMLFormat(template),
                              *common_rdf_formats
                         ])

