from .asgs_view import ASGSView
from myldapi import Register, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import WFSSource
from .common import ASGS

class Meshblock(Register):
    def __init__(self):            
        self.attribute_mappings = [
                AttributeMapping(varname="object_id", 
                                 wfs_attr="MB:OBJECTID"),
                AttributeMapping(varname="albers_area", 
                                 wfs_attr="MB:AREA_ALBERS_SQKM"),
                AttributeMapping(varname="shape_length", 
                                 wfs_attr="MB:Shape_Length"),
                AttributeMapping(varname="shape_area", 
                                 wfs_attr="MB:Shape_Area"),
                AttributeMapping(varname="shape",
                                 wfs_attr="MB:Shape"),
                AttributeMapping(varname="code", 
                                 wfs_attr="MB:MB_CODE_2016"),
                AttributeMapping(varname="category", 
                                 wfs_attr="MB:MB_CATEGORY_CODE_2016"),
                AttributeMapping(varname="category_name",
                                 label="Category", 
                                 predicate=Pred(ASGS.category), 
                                 wfs_attr="MB:MB_CATEGORY_NAME_2016"),
                AttributeMapping(varname="sa1", 
                                 label="Within SA1", 
                                 predicate=Pred(ASGS.isStatisticalAreaLevel1Of, inverse=True, comment="The SA1 this meshblock is within"), 
                                 wfs_attr="MB:SA1_MAINCODE_2016"),
                AttributeMapping(varname="state", 
                                 label="Within State or Territory", 
                                 predicate=Pred(ASGS.isStateOrTerritoryOf, inverse=True, comment="The state this meshblock is within"), 
                                 wfs_attr="MB:STATE_CODE_2016"),
                AttributeMapping(varname="dzn", 
                                 wfs_attr="MB:DZN_CODE_2016"),
                AttributeMapping(varname="ssc",  
                                 wfs_attr="MB:SSC_CODE_2016"),
                AttributeMapping(varname="nrmr",  
                                 wfs_attr="MB:NRMR_CODE_2016"),
                AttributeMapping(varname="add",  
                                 wfs_attr="MB:ADD_CODE_2016"),
            ]

        self.source = WFSSource(
            endpoint="https://geo.abs.gov.au/arcgis/services/ASGS2016/MB/MapServer/WFSServer",
            typename="MB:MB",
            id_prop="MB:MB_CODE_2016",
            ns_map={
                "MB": "WFS"
            },
            attr_map=self.attribute_mappings)

        super().__init__(name = "Meshblock",
                         path = "meshblock",
                         type_uri = "http://linked.data.gov.au/def/asgs#MeshBlock",
                         base_uri = "http://linked.data.gov.au/dataset/asgs2016/meshblock/",
                         views=[
                             ASGSView(self.source)
                         ])    


    def list_uris(self, page=0, page_size=20):
        ids = self.source.get_ids(page, size)
        return [get_uri_for(id) for id in ids]

    def get_count(self):
        return self.source.get_count()
