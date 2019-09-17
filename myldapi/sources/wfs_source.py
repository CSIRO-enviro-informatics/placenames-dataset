import requests
from lxml import etree
from functools import lru_cache
from .source import Source


class WFSSource(Source):
    def __init__(self, endpoint, typename, id_prop, ns_map, attr_map):
        self.endpoint = endpoint
        self.ns_map = ns_map
        self.attr_map = attr_map
        self.typename = typename
        self.id_prop = id_prop

    @lru_cache(maxsize=32)
    def get_object_details(self, uri):
        url = self.query_for_id(id)
        resp = requests.get(url)
        tree = etree.parse(BytesIO(resp.content))  # type lxml._ElementTree
        for am in self.attr_map:
            text = tree.xpath('//{}/text()'.format(am.wfs_attr), namespaces=tree.getroot().nsmap)
            am.value = am.typefunc(text)

        return self.attr_map
            

    @lru_cache(maxsize=1)
    def get_count(self):
        # attempt dynamic, otherwise use fixed value
        pass

    def get_ids(self, startindex, count):
        if startindex + count > self.get_count():
            raise IndexError("Attempting to access more elements than exist")

        url = self.query_for_id(id)
        resp = requests.get(url)
        tree = etree.parse(BytesIO(resp.content))  # type lxml._ElementTree
        return tree.xpath('//{}/text()'.format(self.id_prop), namespaces=tree.getroot().nsmap)

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
