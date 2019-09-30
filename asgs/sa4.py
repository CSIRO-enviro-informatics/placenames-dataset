from .asgs_view import ASGSView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import WFSSource
from .config import ASGS, DATASET_URI, SA4_COUNT
from .common import get_common_attributes, get_geometry_attributes
from .states import StateOrTerritory
from myldapi.utils import RDF_a

class StatisticalAreaLevel4(SourceRegister):
    def __init__(self):       
        ns = "SA4"     
        attribute_mappings = [
                AttributeMapping(varname="code", 
                                 predicate=Pred(ASGS.sa4Maincode2016), 
                                 wfs_attr=f"{ns}:SA4_CODE_2016"),
                AttributeMapping(varname="statisticalArea2Sa29DigitCode", 
                                 predicate=Pred(ASGS.statisticalArea4Sa43DigitCode), 
                                 wfs_attr=f"{ns}:SA4_CODE_2016"),
                AttributeMapping(varname="name", 
                                 label=u"Name", 
                                 predicate=Pred(ASGS.sa4Name2016, comment="The name of this SA4"), 
                                 wfs_attr=f"{ns}:SA4_NAME_2016"),
                AttributeMapping(varname="gccsa", 
                                 label="Greater Capital City Statistical Area", 
                                 predicate=Pred(ASGS.isGreaterCapitalCityStatisticalAreaOf, 
                                                inverse=True,
                                                comment="Greater Capital City Statistical Area",
                                                builder=Pred.node_builder(None, [
                                                        (Pred(RDF_a), ASGS.GreaterCapitalCityStatisticalArea),
                                                        (Pred(ASGS.gccsaCode2016), "gccsa"),
                                                        (Pred(ASGS.greaterCapitalCityStatisticalAreasGccsa5CharacterAlphanumericCode), "gccsa")
                                                    ])), 
                                 wfs_attr=f"{ns}:GCCSA_CODE_2016"),
                AttributeMapping(varname="state", 
                                 label="Within State or Territory", 
                                 predicate=Pred(ASGS.isStateOrTerritoryOf, inverse=True, comment="The state this SA4 is within"), 
                                 converter=AttributeMapping.reg_id_converter(StateOrTerritory),
                                 wfs_attr=f"{ns}:STATE_CODE_2016"),
                *get_common_attributes(ns),
                # *get_geometry_attributes(ns)
            ]

        source = WFSSource(
            endpoint=f"https://geo.abs.gov.au/arcgis/services/ASGS2016/{ns}/MapServer/WFSServer",
            typename=f"{ns}:SA4",
            id_prop=f"{ns}:SA4_CODE_2016",
            ns_map={
                f"{ns}": "WFS"
            },
            count=SA4_COUNT,
            attr_map=attribute_mappings)

        super().__init__(name = "Register of ASGS SA4's",
                         path = "statisticalarealevel4",
                         type_uri = "http://linked.data.gov.au/def/asgs#StatisticalAreaLevel4",
                         type_name = "StatisticalAreaLevel4",
                         base_uri = f"{DATASET_URI}/statisticalarealevel4",
                         views=[
                             ASGSView(source)
                         ], 
                         source=source)    
