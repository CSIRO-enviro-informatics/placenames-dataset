from .views import GNAFView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import DBSource
from .config import GNAF, DATASET_URI, GNAF_CONNECTION
from myldapi.utils import RDF_a, RDFS, GEO
from .address_site import AddressSite
from rdflib import URIRef

class Address(SourceRegister):
    def __init__(self):  
        attribute_mappings = [
                # AttributeMapping(varname="label", 
                #                  label="Label",                                  
                #                  col_name=["gnaf.address_site_geocode.longitude", "gnaf.address_site_geocode.latitude"],
                #                  converter=lambda parameter_list: expression,
                #                  predicate=Pred(RDF{dbschema}.street_locality.label)),
                # AttributeMapping(varname="gnafType", 
                #                  label="GNAF Type",
                #                  predicate=Pred(GNAF.gnafType)),
                AttributeMapping(varname="addressSite", 
                                 label="Address Site",
                                 col_name="gnaf.address_detail.address_site_pid",
                                 converter=AttributeMapping.reg_id_converter(AddressSite),
                                 predicate=Pred(GNAF.hasAddressSite)),
                # AttributeMapping(varname="dateCreated", 
                #                  label="Creation Date",
                #                  predicate=Pred(GNAF.hasDateCreated)),
            ]

 
        dbschema = "gnaf"
        source = DBSource(
            conn_str=GNAF_CONNECTION,
            from_query=f"""{dbschema}.address_detail
                       INNER JOIN {dbschema}.street_locality ON {dbschema}.address_detail.street_locality_pid = {dbschema}.street_locality.street_locality_pid
                       INNER JOIN {dbschema}.locality ON {dbschema}.address_detail.locality_pid = {dbschema}.locality.locality_pid
                       INNER JOIN {dbschema}.address_default_geocode ON {dbschema}.address_detail.address_detail_pid = {dbschema}.address_default_geocode.address_detail_pid                
                       LEFT JOIN codes.geocode ON {dbschema}.address_default_geocode.geocode_type_code = codes.geocode.code           
                       LEFT JOIN codes.gnafconfidence ON CAST({dbschema}.address_detail.confidence AS text) = codes.gnafconfidence.code 
                       LEFT JOIN codes.locality ON {dbschema}.locality.locality_class_code = codes.locality.code 
                       INNER JOIN {dbschema}.address_site ON {dbschema}.address_detail.address_site_pid = {dbschema}.address_site.address_site_pid
                       LEFT JOIN codes.address ON {dbschema}.address_site.address_type = codes.address.code 
                       LEFT JOIN codes.flat ON {dbschema}.address_detail.flat_type_code = codes.flat.code 
                       LEFT JOIN codes.state ON CAST({dbschema}.locality.state_pid AS text) = codes.state.code""",
            id_prop=f"{dbschema}.address_detail.address_detail_pid",
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
