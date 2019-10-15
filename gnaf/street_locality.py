from .views import GNAFView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import DBSource
from .config import GNAF, DATASET_URI
from myldapi.utils import RDF_a, RDFS

class StreetLocality(SourceRegister):
    def __init__(self):  
        attribute_mappings = [
                # I think I would have the RDFS label 
                # AttributeMapping(varname="label", 
                #         label="Label", 
                #         predicate=Pred(RDFS.label)),
                AttributeMapping(varname="name", 
                                 label="Name", 
                                 predicate=Pred(RDFS.hasName)),
                AttributeMapping(varname="streetLine", 
                                 label="Street Line"),
                AttributeMapping(varname="streetType", 
                                 label="Street Type",
                                 converter=AttributeMapping.base_uri_converter("http://linked.data.gov.au/def/gnaf/code/StreetTypes#"),
                                 predicate=Pred(GNAF.hasStreetType)),                                                                  
                AttributeMapping(varname="addressSite", 
                                 label="Address Site",
                                 predicate=Pred(GNAF.hasAddressSite)),
                AttributeMapping(varname="dateCreated", 
                                 label="Creation Date",
                                 predicate=Pred(GNAF.hasDateCreated)),
            ]

        source = DBSource(
            attr_map=attribute_mappings)

        super().__init__(name = "Register of GNAF Addresses",
                         path = "address",
                         type_uri = str(GNAF.Address),
                         type_name = "Address",
                         base_uri = f"{DATASET_URI}/address",
                         views=[
                             GNAFView(source)
                         ], 
                         source=source)    
