from .views import GNAFView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred, AttributeMappingValue
from myldapi.sources import DBSource
from .config import GNAF, DATASET_URI, GNAF_CONNECTION
from myldapi.utils import RDF_a, RDFS, GEO
from rdflib import URIRef

class AddressSite(SourceRegister):
    def __init__(self):  

        geo_code_attrs = [
                AttributeMapping(varname="a_type", 
                                 converter=AttributeMapping.literal_converter(GNAF.Geocode),
                                 predicate=Pred(RDF_a)),
                AttributeMapping(varname="label", 
                                 label="Code Type",
                                 col_name="codes.geocode.preflabel",
                                 predicate=Pred(RDFS.label)),
                AttributeMapping(varname="longitude", 
                                 label="Longitude",
                                 col_name="gnaf.address_site_geocode.longitude",
                                 ),
                AttributeMapping(varname="latitude", 
                                 label="Latitude",
                                 col_name="gnaf.address_site_geocode.latitude",
                                 ),
                AttributeMapping(varname="gnafTypeUri", 
                                 col_name="codes.geocode.uri",
                                 predicate=Pred(GNAF.gnafType)),        
                AttributeMapping(varname="geometry",                                  
                                 col_name=["gnaf.address_site_geocode.longitude", "gnaf.address_site_geocode.latitude"],
                                 converter=wkt_converter,
                                 predicate=Pred(GEO.asWKT)),        
            ]

        attribute_mappings = [
                AttributeMapping(varname="pid", 
                                 label="Address Site PID",
                                 col_name="gnaf.address_site.address_site_pid",
                                 ),
                AttributeMapping(varname="gnafType", 
                                 label="GNAF Type",
                                 col_name="gnaf.address_site.address_type",                                 
                                 ),
                AttributeMapping(varname="gnafTypeUri", 
                                 col_name="codes.address.uri as type_uri",                                 
                                 predicate=Pred(GNAF.gnafType)),
                AttributeMapping(varname="name", 
                                 label="Name",
                                 col_name="gnaf.address_site.address_site_name",
                                 predicate=Pred(RDFS.label)),
                # AttributeMapping(varname="comment", 
                #                  label="Comment",
                #                  predicate=Pred(RDFS.comment)),
                AttributeMapping(varname="geocodes", 
                                 label="Geocodes",
                                 child_attrs=geo_code_attrs,
                                 col_name="gnaf.address_site_geocode.address_site_geocode_pid",
                                 predicate=Pred(GNAF.hasGeometry)),
            ]

        source = DBSource(
            conn_str=GNAF_CONNECTION,
            from_query="""gnaf.address_site
                LEFT JOIN gnaf.address_site_geocode on gnaf.address_site.address_site_pid = gnaf.address_site_geocode.address_site_pid
                LEFT JOIN codes.address on gnaf.address_site.address_type = codes.address.code
                LEFT JOIN codes.geocode on gnaf.address_site_geocode.geocode_type_code = codes.geocode.code""",
            id_prop="gnaf.address_site.address_site_pid",
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

def wkt_converter(vals):
    longitude, latitude = vals
    return AttributeMappingValue('<http://www.opengis.net/def/crs/EPSG/0/4283> POINT({} {})'.format(
            longitude, latitude
        ), None)