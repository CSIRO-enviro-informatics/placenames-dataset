import requests
from lxml import etree

class WFSSource():
    def __init__(self, endpoint, mapping):
        self.endpoint = endpoint
        self.mapping = mapping

    def get_object_details(self, id):
        url = cls.construct_wfs_query_for_index(asgs_type, startindex, count)
        resp = requests.get(url)
        tree = etree.parse(BytesIO(resp.content)) #type lxml._ElementTree

    def get_count(self):
        pass

    def construct_wfs_query_for_index(self):
        uri_template = self.endpoint +\
                       '?service=wfs&version=2.0.0&request=GetFeature&typeName={typename}' \
                       '&propertyName={propertyname}' \
                       '&sortBy={propertyname}&startIndex={startindex}&count={count}'