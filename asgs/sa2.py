from .asgs_view import ASGSView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import WFSSource
from .config import ASGS, DATASET_URI, SA2_COUNT
from .common import get_common_attributes, get_geometry_attributes
from .sa3 import StatisticalAreaLevel3
from .states import StateOrTerritory
class StatisticalAreaLevel2(SourceRegister):
    def __init__(self):       
        ns = "SA2"     
        attribute_mappings = [
                AttributeMapping(varname="code", 
                                 predicate=Pred(ASGS.sa2Maincode2016), 
                                 wfs_attr=f"{ns}:SA2_MAINCODE_2016"),
                AttributeMapping(varname="statisticalArea2Sa29DigitCode", 
                                 predicate=Pred(ASGS.statisticalArea2Sa29DigitCode), 
                                 wfs_attr=f"{ns}:SA2_MAINCODE_2016"),
                AttributeMapping(varname="name", 
                                 label="Name", 
                                 predicate=Pred(ASGS.sa2Name2016, comment="The name of this SA2"), 
                                 wfs_attr=f"{ns}:SA2_NAME_2016"),
                AttributeMapping(varname="sa3", 
                                 label="Within SA3", 
                                 predicate=Pred(ASGS.isStatisticalAreaLevel3Of, inverse=True, comment="The SA3 this SA2 is within"), 
                                 converter=AttributeMapping.reg_id_converter(StatisticalAreaLevel3),
                                 wfs_attr=f"{ns}:SA3_CODE_2016"),
                AttributeMapping(varname="state", 
                                 label="Within State or Territory", 
                                 predicate=Pred(ASGS.isStateOrTerritoryOf, inverse=True, comment="The state this SA2 is within"), 
                                 converter=AttributeMapping.reg_id_converter(StateOrTerritory),
                                 wfs_attr=f"{ns}:STATE_CODE_2016"),
                *get_common_attributes(ns),
                *get_geometry_attributes(ns)
            ]

        source = WFSSource(
            endpoint=f"https://geo.abs.gov.au/arcgis/services/ASGS2016/{ns}/MapServer/WFSServer",
            typename=f"{ns}:SA2",
            id_prop=f"{ns}:SA2_MAINCODE_2016",
            ns_map={
                f"{ns}": "WFS"
            },
            count=SA2_COUNT,
            attr_map=attribute_mappings)

        super().__init__(name = "Register of ASGS SA2's",
                         path = "statisticalarealevel2",
                         type_uri = "http://linked.data.gov.au/def/asgs#StatisticalAreaLevel2",
                         type_name = "StatisticalAreaLevel2",
                         base_uri = f"{DATASET_URI}/statisticalarealevel2",
                         views=[
                             ASGSView(source)
                         ], 
                         source=source)    
