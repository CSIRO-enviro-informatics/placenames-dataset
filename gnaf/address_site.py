from .views import GNAFView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import DBSource
from .config import GNAF, DATASET_URI, GNAF_CONNECTION
from myldapi.utils import RDF_a, RDFS

class AddressSite(SourceRegister):
    def __init__(self):  
        attribute_mappings = [
                AttributeMapping(varname="gnafType", 
                                 label="GNAF Type",
                                 col_name="address_type",
                                 predicate=Pred(GNAF.gnafType)),
                # AttributeMapping(varname="geometry", 
                #                  label="Geometry",
                #                  predicate=Pred(GNAF.hasGeometry)),
                # AttributeMapping(varname="comment", 
                #                  label="Comment",
                #                  predicate=Pred(RDFS.comment)),
            ]

        source = DBSource(
            conn_str=GNAF_CONNECTION,
            from_query="gnaf.address_site",
            id_prop="address_site_pid",
            attr_map=attribute_mappings)

        super().__init__(name = "Register of GNAF Address Sites",
                         path = "addressSite",
                         type_uri = str(GNAF.AddressSite),
                         type_name = "Address Site",
                         base_uri = f"{DATASET_URI}/addressSite",
                         views=[
                             GNAFView(source)
                         ], 
                         source=source)    
