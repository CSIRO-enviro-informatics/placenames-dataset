from myldapi import AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.utils import GEOX, DATA, QB4ST, CRS_EPSG, GML, GEO, RDF_a, \
                          take_xml_as_string_element_converter, \
                          gml_extract_geom_to_geojson
from rdflib import URIRef
from decimal import Decimal


def get_common_attributes(ns):
    return [
        AttributeMapping(varname="object_id", 
                                 wfs_attr=f"{ns}:OBJECTID"),
        AttributeMapping(varname="albers_area_3577", 
                         label="Albers Area (m\u00B2)",
                         predicate=Pred(GEOX.hasAreaM2, 
                                        builder=Pred.node_builder(None, [
                                            (Pred(DATA.value), "albers_area_3577"),
                                            (Pred(QB4ST.crs), CRS_EPSG["3577"])
                                        ])),   
                         typefunc=Decimal,
                         converter=AttributeMapping.basic_converter(lambda val: val * 1000000), #convert to m^2
                         wfs_attr=f"{ns}:AREA_ALBERS_SQKM"),
        AttributeMapping(varname="shape_area", 
                         label="Shape Area (m\u00B2)",
                         predicate=Pred(GEOX.hasAreaM2, 
                                        builder=Pred.node_builder(None, [
                                            (Pred(DATA.value), "shape_area"),
                                            (Pred(QB4ST.crs), CRS_EPSG["3857"])
                                        ])),   
                         typefunc=Decimal,
                         wfs_attr=f"{ns}:Shape_Area"),
        AttributeMapping(varname="shape_length", 
                         label="Shape Length (m)",
                         typefunc=Decimal,
                         wfs_attr=f"{ns}:Shape_Length"),
    ]

def get_geometry_attributes(ns): 
    return [
        AttributeMapping(varname="geometry",
                         wfs_attr=f"{ns}:Shape",
                         wfs_element_converter=take_xml_as_string_element_converter,
                         predicate=Pred(GEO.hasGeometry, 
                                        builder=Pred.node_builder(None, [
                                            (Pred(RDF_a), GEO.Geometry),
                                            (Pred(GML.asGML), "geometry", GML.gmlLiteral)
                                        ])),   
                         ),
        AttributeMapping(varname="geojson",
                         wfs_attr=f"{ns}:Shape",
                         wfs_element_converter=lambda node, crs: gml_extract_geom_to_geojson(node, parent_srs=crs),
                         )
    ]
    
