from .views import ASGSView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import WFSSource
from .config import ASGS, DATASET_URI, MESHBLOCK_COUNT
from .sa1 import StatisticalAreaLevel1
from .states import StateOrTerritory
from .common import get_common_attributes, get_geometry_attributes
from myldapi.utils import RDF_a
class Meshblock(SourceRegister):
    def __init__(self):  
        ns = "MB"
        attribute_mappings = [
                AttributeMapping(varname="code", 
                                 predicate=Pred(ASGS.mbCode2016), 
                                 wfs_attr=f"{ns}:MB_CODE_2016"),
                AttributeMapping(varname="category", 
                                 wfs_attr=f"{ns}:MB_CATEGORY_CODE_2016"),
                AttributeMapping(varname="category_name",
                                 label="Category", 
                                 predicate=Pred(ASGS.category), 
                                 wfs_attr=f"{ns}:MB_CATEGORY_NAME_2016"),
                AttributeMapping(varname="sa1", 
                                 label="Within SA1", 
                                 predicate=Pred(ASGS.isStatisticalAreaLevel1Of, inverse=True, comment="The SA1 this meshblock is within"), 
                                 converter=AttributeMapping.reg_id_converter(StatisticalAreaLevel1),
                                 wfs_attr=f"{ns}:SA1_MAINCODE_2016"),
                AttributeMapping(varname="state", 
                                 label="Within State or Territory", 
                                 predicate=Pred(ASGS.isStateOrTerritoryOf, inverse=True, comment="The state this meshblock is within"), 
                                 converter=AttributeMapping.reg_id_converter(StateOrTerritory),
                                 wfs_attr=f"{ns}:STATE_CODE_2016"),
                AttributeMapping(varname="dzn", 
                                 label="Within Destination Zone",
                                 predicate=Pred(ASGS.contains, inverse=True, comment="Destination Zone meshblock is within", 
                                                builder=Pred.node_builder(None, [
                                                        (Pred(RDF_a), ASGS.DestinationZone),
                                                        (Pred(ASGS.dznCode2016), "dzn")
                                                    ])),                                                
                                 wfs_attr=f"{ns}:DZN_CODE_2016"),
                AttributeMapping(varname="ssc",
                                 label="Within StateSuburb Code", 
                                 predicate=Pred(ASGS.contains, inverse=True, comment="StateSuburb Code meshblock is within", 
                                                builder=Pred.node_builder(None, [
                                                        (Pred(RDF_a), ASGS.StateSuburb),
                                                        (Pred(ASGS.sscCode2016), "ssc")
                                                    ])),                                                
                                 wfs_attr=f"{ns}:SSC_CODE_2016"),
                AttributeMapping(varname="nrmr",
                                 label="Within Natural Resource Management Region",
                                 predicate=Pred(ASGS.contains, inverse=True, comment="NRMR meshblock is within", 
                                                builder=Pred.node_builder(None, [
                                                        (Pred(RDF_a), ASGS.NaturalResourceManagementRegion),
                                                        (Pred(ASGS.nrmrCode2016), "nrmr")
                                                    ])),                                                
                                 wfs_attr=f"{ns}:NRMR_CODE_2016"),
                # AttributeMapping(varname="add",  
                #                  wfs_attr=f"{ns}:ADD_CODE_2016"),
                *get_common_attributes(ns),
                *get_geometry_attributes(ns)
            ]

        source = WFSSource(
            endpoint=f"https://geo.abs.gov.au/arcgis/services/ASGS2016/{ns}/MapServer/WFSServer",
            typename=f"{ns}:MB",
            id_prop=f"{ns}:MB_CODE_2016",
            ns_map={
                f"{ns}": "WFS"
            },
            default_crs="EPSG:3857",
            attr_map=attribute_mappings)

        super().__init__(name = "Register of ASGS Meshblocks",
                         path = "meshblock",
                         type_uri = "http://linked.data.gov.au/def/asgs#MeshBlock",
                         type_name = "Meshblock",
                         base_uri = f"{DATASET_URI}/meshblock",
                         views=[
                             ASGSView(source)
                         ], 
                         source=source)    
