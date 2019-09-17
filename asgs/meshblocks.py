from ..myldapi.register import Register
from asgs_view import ASGSView

class Meshblock(Register):
    def __init__(self):
        super().__init__(name = "Meshblock"
                         path = "meshblock"
                         type_uri = "http://linked.data.gov.au/def/asgs#MeshBlock"
                         base_uri = "http://linked.data.gov.au/dataset/asgs2016/meshblock/",
                         views=[
                             ASGSView(source)
                         ])
            
        self.attribute_mappings = [
                AttributeMapping(varname="object_id", predicates=[], wfs_attr="{WFS}OBJECTID"),
                AttributeMapping(varname="albers_area", predicates=[], wfs_attr="{WFS}AREA_ALBERS_SQKM"),
                AttributeMapping(varname="shape_length", predicates=[], wfs_attr="{WFS}Shape_Length"),
                AttributeMapping(varname="shape_area", predicates=[], wfs_attr="{WFS}Shape_Area"),
                AttributeMapping(varname="shape", predicates=[], wfs_attr="{WFS}Shape"),
                AttributeMapping(varname="code", predicates=[], wfs_attr="{WFS}MB_CODE_2016"),
                AttributeMapping(varname="category", predicates=[], wfs_attr="{WFS}MB_CATEGORY_CODE_2016"),
                AttributeMapping(varname="category_name", predicates=[], wfs_attr="{WFS}MB_CATEGORY_NAME_2016"),
                AttributeMapping(varname="sa1", predicates=[], wfs_attr="{WFS}SA1_MAINCODE_2016"),
                AttributeMapping(varname="state", predicates=[], wfs_attr="{WFS}STATE_CODE_2016"),
                AttributeMapping(varname="dzn", predicates=[], wfs_attr="{WFS}DZN_CODE_2016"),
                AttributeMapping(varname="ssc", predicates=[], wfs_attr="{WFS}SSC_CODE_2016"),
                AttributeMapping(varname="nrmr", predicates=[], wfs_attr="{WFS}NRMR_CODE_2016"),
                AttributeMapping(varname="add", predicates=[], wfs_attr="{WFS}ADD_CODE_2016"),
            ]

        source = WFSSource(
            endpoint="https://geo.abs.gov.au/arcgis/services/ASGS2016/MB/MapServer/WFSServer",
            typename="MB:MB",
            id_prop="MB:MB_CODE_2016",
            ns_map={
                "MB": "WFS"
            },
            attr_map=self.attribute_mappings)

        


    def get_graph_for_id(self, id):
        deets = self.source.get_object_details(id)

    def create_list(self, uri, page, page_size):
        return []
