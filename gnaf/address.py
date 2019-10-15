from .views import GNAFView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import DBSource
from .config import GNAF, DATASET_URI
from myldapi.utils import RDF_a, RDFS
from .address_site import AddressSite

class Address(SourceRegister):
    def __init__(self):  
        attribute_mappings = [
                AttributeMapping(varname="label", 
                                 label="Label", 
                                 predicate=Pred(RDFS.label)),
                AttributeMapping(varname="gnafType", 
                                 label="GNAF Type",
                                 predicate=Pred(GNAF.gnafType)),
                AttributeMapping(varname="addressSite", 
                                 label="Address Site",
                                 converter=AttributeMapping.reg_id_converter(AddressSite)
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
