from .asgs_view import ASGSView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import WFSSource
from .config import ASGS, DATASET_URI, SA3_COUNT
from .common import get_common_attributes, get_geometry_attributes
from .states import StateOrTerritory
from .sa4 import StatisticalAreaLevel4

class StatisticalAreaLevel3(SourceRegister):
    def __init__(self):       
        ns = "SA3"     
        attribute_mappings = [
                AttributeMapping(varname="code", 
                                 predicate=Pred(ASGS.sa3Maincode2016), 
                                 wfs_attr=f"{ns}:SA3_CODE_2016"),
                AttributeMapping(varname="statisticalArea2Sa29DigitCode", 
                                 predicate=Pred(ASGS.statisticalArea3Sa35DigitCode), 
                                 wfs_attr=f"{ns}:SA3_CODE_2016"),
                AttributeMapping(varname="name", 
                                 label="Name", 
                                 predicate=Pred(ASGS.sa3Name2016, comment="The name of this SA3"), 
                                 wfs_attr=f"{ns}:SA3_NAME_2016"),
                AttributeMapping(varname="sa4", 
                                 label="Within SA4", 
                                 predicate=Pred(ASGS.isStatisticalAreaLevel4Of, inverse=True, comment="The SA4 this SA3 is within"), 
                                 converter=AttributeMapping.reg_id_converter(StatisticalAreaLevel4),
                                 wfs_attr=f"{ns}:SA4_CODE_2016"),
                AttributeMapping(varname="state", 
                                 label="Within State or Territory", 
                                 predicate=Pred(ASGS.isStateOrTerritoryOf, inverse=True, comment="The state this SA3 is within"), 
                                 converter=AttributeMapping.reg_id_converter(StateOrTerritory),
                                 wfs_attr=f"{ns}:STATE_CODE_2016"),
                *get_common_attributes(ns),
                *get_geometry_attributes(ns)
            ]

        source = WFSSource(
            endpoint=f"https://geo.abs.gov.au/arcgis/services/ASGS2016/{ns}/MapServer/WFSServer",
            typename=f"{ns}:SA3",
            id_prop=f"{ns}:SA3_CODE_2016",
            ns_map={
                f"{ns}": "WFS"
            },
            count=SA3_COUNT,
            attr_map=attribute_mappings)

        super().__init__(name = "Register of ASGS SA3's",
                         path = "statisticalarealevel3",
                         type_uri = "http://linked.data.gov.au/def/asgs#StatisticalAreaLevel3",
                         type_name = "StatisticalAreaLevel3",
                         base_uri = f"{DATASET_URI}/statisticalarealevel3",
                         views=[
                             ASGSView(source)
                         ], 
                         source=source)    
