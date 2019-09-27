from myldapi import AttributeMapping, AttributeMappingPredicate as Pred


def get_common_attributes(ns):
    return [
        AttributeMapping(varname="object_id", 
                                 wfs_attr=f"{ns}:OBJECTID"),
        AttributeMapping(varname="albers_area", 
                         wfs_attr=f"{ns}:AREA_ALBERS_SQKM"),
        AttributeMapping(varname="shape_length", 
                         wfs_attr=f"{ns}:Shape_Length"),
        AttributeMapping(varname="shape_area", 
                         wfs_attr=f"{ns}:Shape_Area"),
        AttributeMapping(varname="shape",
                         wfs_attr=f"{ns}:Shape")
    ]
