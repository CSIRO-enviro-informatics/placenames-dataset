from .asgs_view import ASGSView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import WFSSource
from .config import ASGS, DATASET_URI, STATE_COUNT
from .common import get_common_attributes

class StateOrTerritory(SourceRegister):
    def __init__(self):            
        ns = "STATE"
        attribute_mappings = [                                             
                AttributeMapping(varname="code", 
                                 wfs_attr=f"{ns}:STATE_CODE_2016"),
                AttributeMapping(varname="name", 
                                 label="Name", 
                                 wfs_attr=f"{ns}:STATE_NAME_2016"),
                AttributeMapping(varname="name_abbrev", 
                                 label="Abbreviated name", 
                                 wfs_attr=f"{ns}:STATE_NAME_ABBREV_2016"),
                *get_common_attributes("STATE"),
            ]

        source = WFSSource(
            endpoint=f"https://geo.abs.gov.au/arcgis/services/ASGS2016/{ns}/MapServer/WFSServer",
            typename=f"{ns}:STATE",
            id_prop=f"{ns}:STATE_CODE_2016",
            ns_map={
                f"{ns}": "WFS"
            },
            count=STATE_COUNT,
            attr_map=attribute_mappings)

        super().__init__(name = "Register of ASGS States and Territories",
                         path = "stateorterritory",
                         type_uri = "http://linked.data.gov.au/def/asgs#StateOrTerritory",
                         type_name = "StateOrTerritory",
                         base_uri = f"{DATASET_URI}/stateorterritory",
                         views=[
                             ASGSView(source)
                         ], 
                         source=source)    
