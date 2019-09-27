from myldapi import AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.utils import GEOX, DATA, QB4ST, CRS_EPSG
from rdflib import URIRef
from decimal import Decimal


def get_common_attributes(ns):
    return [
        AttributeMapping(varname="object_id", 
                                 wfs_attr=f"{ns}:OBJECTID"),
        AttributeMapping(varname="albers_area_3577", 
                         predicate=Pred(GEOX.hasAreaM2, 
                                        builder=Pred.node_builder(None, [
                                            (Pred(DATA.value), "albers_area_3577"),
                                            (Pred(QB4ST.crs), CRS_EPSG["3577"])
                                        ])),   
                         typefunc=Decimal,
                         converter=AttributeMapping.basic_converter(lambda val: val * 1000000), #convert to m^2
                         wfs_attr=f"{ns}:AREA_ALBERS_SQKM"),
        AttributeMapping(varname="shape_length", 
                         wfs_attr=f"{ns}:Shape_Length"),
        AttributeMapping(varname="shape_area", 
                         predicate=Pred(GEOX.hasAreaM2, 
                                        builder=Pred.node_builder(None, [
                                            (Pred(DATA.value), "shape_area"),
                                            (Pred(QB4ST.crs), CRS_EPSG["3857"])
                                        ])),   
                         typefunc=Decimal,
                         wfs_attr=f"{ns}:Shape_Area"),
        AttributeMapping(varname="shape",
                         wfs_attr=f"{ns}:Shape")
    ]

