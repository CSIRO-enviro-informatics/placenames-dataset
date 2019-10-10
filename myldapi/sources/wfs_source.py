import requests
from lxml import etree
from functools import lru_cache
from .source import Source
from io import StringIO, BytesIO
from ..utils import id_from_uri
from ..attr_mapping import AttributeMapping


class WFSSource(Source):
    def __init__(self, endpoint, typename, id_prop, ns_map, attr_map, count=None):
        self.endpoint = endpoint
        self.ns_map = ns_map
        self.attr_map = attr_map
        self.typename = typename
        self.id_prop = id_prop
        self.count = count

    def get_many_object_details(self, id_list):
        obj_attr_list = []
        url = self.query_for_objects(id_list)
        resp = requests.post(self.endpoint, data=url)
        #should check for an exception here and blow out when making a bad request.

        tree = etree.parse(BytesIO(resp.content))  # type lxml._ElementTree
        object_results = tree.xpath(f"//{self.typename}", namespaces=tree.getroot().nsmap)

        for obj_el in object_results:
            new_tree = etree.ElementTree(obj_el)
            attr_pairings = []
            for am in self.attr_map:
                value = self.get_attr_from_tree(new_tree, am)
                attr_pairings.append((am, value))
            
            id_val = self.get_attr_from_tree(new_tree, AttributeMapping('id', wfs_attr=self.id_prop))
            obj_attr_list.append((id_val.value, attr_pairings))

        return obj_attr_list

    def get_attr_from_tree(self, tree, am):
        results = tree.xpath(f"//{am.wfs_attr}", namespaces=tree.getroot().nsmap)        
        if len(results) > 1:
            raise NotImplementedError("We currently dont handle WFS objects with multiple attributes of the same name")
        elif len(results) == 0:
            value = None
        else:
            if hasattr(am, "element_converter"):
                result = am.element_converter(results[0])
            else:
                result = results[0].text #default to just take the te
            value = am.create_value(result)
 
        return value


    @lru_cache(maxsize=1)
    def get_count(self):
        if self.count:
            return self.count

        url = self.query_for_count()
        resp = requests.post(self.endpoint, data=url)
        tree = etree.parse(BytesIO(resp.content))  # type lxml._ElementTree
        return int(tree.getroot().attrib['numberOfFeatures'])

    def get_ids(self, startindex, count):
        if startindex + count > self.get_count():
            raise IndexError("Attempting to access more elements than exist")

        url = self.query_for_ids(startindex, count)
        resp = requests.get(url)
        tree = etree.parse(BytesIO(resp.content))  # type lxml._ElementTree
        return tree.xpath('//{}/text()'.format(self.id_prop), namespaces=tree.getroot().nsmap)

    def query_for_count(self):
        post_template = """<wfs:GetFeature service="WFS" version="1.1.0"
resultType="hits"
xmlns:wfs="http://www.opengis.net/wfs"
xmlns:ogc="http://www.opengis.net/ogc"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.opengis.net/wfs
                    http://schemas.opengis.net/wfs/1.0.0/WFS-basic.xsd">
<wfs:Query typeNames="{self.typename}">
        <wfs:PropertyName>{self.id_prop}</wfs:PropertyName>
</wfs:Query>
</wfs:GetFeature>"""

        return post_template.format(**vars(self), **locals())
        
    # def query_for_object(self, id):
    #     property_list = [am.wfs_attr for am in self.attr_map if hasattr(am, 'wfs_attr')]
    #     property_list.append(self.id_prop)
    #     property_list = list(dict.fromkeys(property_list)) #remove duplicates
    #     property_names = ",".join(property_list)
    #     uri_template = self.endpoint + \
    #         '?service=wfs&version=2.0.0&request=GetFeature&typeName={self.typename}' \
    #         '&propertyName={property_names}' \
    #         '&Filter=<ogc:Filter>' \
    #             '<ogc:PropertyIsEqualTo>' \
    #                 '<ogc:PropertyName>{self.id_prop}</ogc:PropertyName>' \
    #                 '<ogc:Literal>{id}</ogc:Literal>' \
    #             '</ogc:PropertyIsEqualTo>' \
    #         '</ogc:Filter>'
    #     return uri_template.format(**vars(self), **locals())

    def query_for_objects(self, id_list):
        property_list = [am.wfs_attr for am in self.attr_map if hasattr(am, 'wfs_attr')]
        property_list.append(self.id_prop)
        property_list = list(dict.fromkeys(property_list)) #remove duplicates
        property_names = [f'<wfs:PropertyName>{prop}</wfs:PropertyName>' for prop in property_list]
        property_filter = "".join(property_names)

        query_tpl = '<ogc:PropertyIsEqualTo>' \
                        f'<ogc:PropertyName>{self.id_prop}</ogc:PropertyName>' \
                        '<ogc:Literal>{val}</ogc:Literal>' \
                    '</ogc:PropertyIsEqualTo>' 
        query_list = [query_tpl.format(val=id) for id in id_list]
        query = "".join(query_list)
        
        if len(query_list) > 1:
            query = f"""<ogc:Or>
                {query}
            </ogc:Or>"""

        post_template = """<wfs:GetFeature service="WFS" version="1.1.0"
  xmlns:wfs="http://www.opengis.net/wfs"
  xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.opengis.net/wfs
                      http://schemas.opengis.net/wfs/1.0.0/WFS-basic.xsd">
  <wfs:Query typeNames="{self.typename}">
        {property_filter}
        <ogc:Filter>
            {query}
        </ogc:Filter>
  </wfs:Query>
</wfs:GetFeature>"""

        return post_template.format(**vars(self), **locals())

    def query_for_ids(self, startindex, take_count):
        #get value for paging the registry
        uri_template = self.endpoint +\
            '?service=wfs&version=2.0.0&request=GetFeature&typeName={self.typename}' \
            '&propertyName={self.id_prop}' \
            '&sortBy={self.id_prop}&startIndex={startindex}&count={take_count}'

        return uri_template.format(**vars(self), **locals())

