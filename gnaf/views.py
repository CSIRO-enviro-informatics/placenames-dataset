from myldapi.views import SourceView
from myldapi.formats import HTMLFormat, common_rdf_formats
from myldapi.utils import DEFAULT_TEMPLATE_OBJECT
from myldapi.sources import Source


class GNAFView(SourceView):
    def __init__(self, source, template=None):
        if template == None:
            template = DEFAULT_TEMPLATE_OBJECT

        super().__init__(name="GNAF",
                         key="gnaf",
                         comment="Basic properties conforming to the PSMA G-NAF Ontologoy",
                         source=source,
                         profile_uri="http://reference.data.gov.au/def/ont/gnaf/",
                         formats=[
                              HTMLFormat(template),
                              *common_rdf_formats
                         ])


class LociView(SourceView):
    def __init__(self, source, template=None):
        if template == None:
            template = DEFAULT_TEMPLATE_OBJECT

        super().__init__(name="GNAF Loci View",
                         key="loci",
                         comment="A stripped back version of the GNAF for the Loci-Cache",
                         source=source,
                         profile_uri="http://linked.data.gov.au/def/loci_dataset",
                         formats=[
                              *common_rdf_formats
                         ])