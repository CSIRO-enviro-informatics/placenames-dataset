from .asgs_view import ASGSView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import WFSSource
from .config import ASGS, DATASET_URI, SA1_COUNT
from .common import get_common_attributes

class StatisticalAreaLevel1(SourceRegister):
    def __init__(self):       
        ns = "SA1"     
        attribute_mappings = [
                AttributeMapping(varname="code", 
                                 predicate=Pred(ASGS.sa1Maincode2016), 
                                 wfs_attr=f"{ns}:SA1_MAINCODE_2016"),
                AttributeMapping(varname="code", 
                                 predicate=Pred(ASGS.statisticalArea1Sa111DigitCode), 
                                 wfs_attr=f"{ns}:SA1_MAINCODE_2016"),
                AttributeMapping(varname="sa2", 
                                 label="Within SA2", 
                                 predicate=Pred(ASGS.isStatisticalAreaLevel2Of, inverse=True, comment="The SA2 this SA1 is within"), 
                                 wfs_attr=f"{ns}:SA2_MAINCODE_2016"),
                AttributeMapping(varname="state", 
                                 label="Within State or Territory", 
                                 predicate=Pred(ASGS.isStateOrTerritoryOf, inverse=True, comment="The state this SA1 is within"), 
                                 wfs_attr=f"{ns}:STATE_CODE_2016"),
                *get_common_attributes(ns),
            ]

        source = WFSSource(
            endpoint=f"https://geo.abs.gov.au/arcgis/services/ASGS2016/{ns}/MapServer/WFSServer",
            typename=f"{ns}:SA1",
            id_prop=f"{ns}:SA1_MAINCODE_2016",
            ns_map={
                f"{ns}": "WFS"
            },
            count=SA1_COUNT,
            attr_map=attribute_mappings)

        super().__init__(name = "Register of ASGS SA1's",
                         path = "statisticalarealevel1",
                         type_uri = "http://linked.data.gov.au/def/asgs#StatisticalAreaLevel1",
                         type_name = "StatisticalAreaLevel1",
                         base_uri = f"{DATASET_URI}/statisticalarealevel1",
                         views=[
                             ASGSView(source)
                         ], 
                         source=source)    
