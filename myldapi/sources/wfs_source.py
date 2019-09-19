import requests
from lxml import etree
from functools import lru_cache
from .source import Source
from io import StringIO, BytesIO
from ..utils import id_from_uri


class WFSSource(Source):
    def __init__(self, endpoint, typename, id_prop, ns_map, attr_map, count=None):
        self.endpoint = endpoint
        self.ns_map = ns_map
        self.attr_map = attr_map
        self.typename = typename
        self.id_prop = id_prop
        self.count = count

    @lru_cache(maxsize=32)
    def get_object_details(self, uri):
        attr_pairings = []
        id = id_from_uri(uri)
        url = self.query_for_id(id)
        resp = requests.get(url)
        tree = etree.parse(BytesIO(resp.content))  # type lxml._ElementTree
        for am in self.attr_map:
            results = tree.xpath('//{}/text()'.format(am.wfs_attr), namespaces=tree.getroot().nsmap)
            if len(results) > 1:
                raise NotImplementedError("We currently dont handle WFS objects with multiple attributes of the same name")
            elif len(results) == 0:
                value = None
            else: 
                value = am.create_value(results[0])
            attr_pairings.append((am, value))

        return attr_pairings
            

    @lru_cache(maxsize=1)
    def get_count(self):
        if self.count:
            return self.count
        raise NotImplemented("Must provide a way to access the count from the WFS")

    def get_ids(self, startindex, count):
        if startindex + count > self.get_count():
            raise IndexError("Attempting to access more elements than exist")

        url = self.query_for_id(id)
        resp = requests.get(url)
        tree = etree.parse(BytesIO(resp.content))  # type lxml._ElementTree
        return tree.xpath('//{}/text()'.format(self.id_prop), namespaces=tree.getroot().nsmap)

    def query_for_id(self, id):
        uri_template = self.endpoint + \
            '?service=wfs&version=2.0.0&request=GetFeature&typeName={self.typename}' \
            '&Filter=<ogc:Filter>' \
                '<ogc:PropertyIsEqualTo>' \
                    '<ogc:PropertyName>{self.id_prop}</ogc:PropertyName>' \
                    '<ogc:Literal>{id}</ogc:Literal>' \
                '</ogc:PropertyIsEqualTo>' \
            '</ogc:Filter>'
        return uri_template.format(**vars(self), **locals())

    def query_for_ids(self, startindex, count):
        #get value for paging the registry
        uri_template = self.endpoint +\
            '?service=wfs&version=2.0.0&request=GetFeature&typeName={self.typename}' \
            '&propertyName={self.id_prop}' \
            '&sortBy={self.id_prop}&startIndex={startindex}&count={count}'

        return uri_template.format(**vars(self), **locals())
