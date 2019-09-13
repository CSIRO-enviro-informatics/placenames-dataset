import requests
from lxml import etree


class WFSSource():
    def __init__(self, endpoint, typename, id_prop, mapping):
        self.endpoint = endpoint
        self.mapping = mapping
        self.typename = typename
        self.id_prop = id_prop

    def get_object_details(self, id):
        url = self.query_for_id(id)
        resp = requests.get(url)
        tree = etree.parse(BytesIO(resp.content))  # type lxml._ElementTree


    def get_count(self):
        # attempt dynamic, otherwise use fixed value
        pass

    def get_ids(self, startindex, count):
        url = self.query_for_id(id)
        resp = requests.get(url)
        tree = etree.parse(BytesIO(resp.content))  # type lxml._ElementTree
        items = tree.xpath('//{}/text()'.format(self.id_prop), namespaces=tree.getroot().nsmap)
        return items


    def query_for_id(self, id):
        uri_template = self.endpoint + \
            '?service=wfs&version=2.0.0&request=GetFeature&typeName={typename}' \
            '&Filter=<ogc:Filter>' \
                '<ogc:PropertyIsEqualTo>' \
                    '<ogc:PropertyName>{id_prop}</ogc:PropertyName>' \
                    '<ogc:Literal>{id}</ogc:Literal>' \
                '</ogc:PropertyIsEqualTo>' \
            '</ogc:Filter>'
        return uri_template.format(**vars(self), **locals())

    def query_for_ids(self, startindex, count):
        #get value for paging the registry
        uri_template = self.endpoint +\
            '?service=wfs&version=2.0.0&request=GetFeature&typeName={typename}' \
            '&propertyName={id_prop}' \
            '&sortBy={id_prop}&startIndex={startindex}&count={count}'

        return uri_template.format(**vars(self), **locals())
