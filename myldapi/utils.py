import rdflib
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD
import lxml

GEO = Namespace("http://www.opengis.net/ont/geosparql#")
GEOX = Namespace("http://linked.data.gov.au/def/geox#")
GML = Namespace("http://www.opengis.net/ont/gml#")
OGC = Namespace("http://www.opengis.net/")
DATA = Namespace("http://linked.data.gov.au/def/datatype/")
CRS_OGC = Namespace("http://www.opengis.net/def/crs/OGC/1.3/")
CRS_EPSG = Namespace("http://www.opengis.net/def/crs/EPSG/0/")
QB4ST = Namespace("http://www.w3.org/ns/qb4st/")

RDF_a = RDF.term('type')

PACKAGE_NAME = "myldapi"

DEFAULT_TEMPLATE_HOME = "{}/home.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_ABOUT = "{}/about.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_ALTERNATES = "{}/alternates.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_OBJECT = "{}/object.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_REGISTER = "{}/register.html".format(PACKAGE_NAME)
DEFAULT_TEMPLATE_ROFR = "{}/registers.html".format(PACKAGE_NAME)

DEFAULT_PAGE_SIZE = 20

def id_from_uri(uri):
    base, objectId = uri.rsplit('/', 1)
    return objectId

def base_from_uri(uri):
    base, objectId = uri.rsplit('/', 1)
    return base

def check_config(name, app):
    if not name in app.config:
        raise ValueError(f"{name} must be set in the config pre-initialistaion of {PACKAGE_NAME}")

def find_prop(pairs, varname):
    return next(((am, v) for am, v in pairs if am.varname == varname), None)

def bind_common(graph):
    graph.bind('geo', GEO)
    graph.bind('geox', GEOX)
    graph.bind('data', DATA)
    graph.bind('ogc', OGC)
    graph.bind('gml', GML)
    graph.bind('qb4st', QB4ST)
    graph.bind('rdfs', QB4ST)


def take_xml_as_string_element_converter(lxml_element):
    if len(lxml_element) != 1:
        raise ValueError("Only works with a single child")
    return lxml.etree.tostring(lxml_element[0], xml_declaration=False, pretty_print=True, encoding=str)



def chunks(source, length):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(source), length):
        yield source[i:i + length]

def gml_extract_geom_to_geojson(node, recursion=0, parent_srs=None):
    """

    :param node:
    :type node: etree._Element
    :return:
    """

    ns = {
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'gml': "http://www.opengis.net/gml/3.2"
    }

    if recursion >= 10:
        return []

    if parent_srs is None:
        default_srs = "EPSG:4326"
    else:
        default_srs = parent_srs

    MultiSurface = "{{{}}}MultiSurface".format(ns['gml'])
    surface_member_tag = "{{{}}}surfaceMember".format(ns['gml'])
    Polygon = "{{{}}}Polygon".format(ns['gml'])
    exterior_tag = "{{{}}}exterior".format(ns['gml'])
    interior_tag = "{{{}}}interior".format(ns['gml'])
    LinearRing = "{{{}}}LinearRing".format(ns['gml'])
    posList = "{{{}}}posList".format(ns['gml'])
    pos = "{{{}}}pos".format(ns['gml'])

    geom = next(node.iterchildren())  # type: etree._Element
    if geom.tag == "something_multigeometry":
        srs_dims = int(geom.get('srsDimension', 2))
        srs_name = geom.get('srsName', default_srs) #4326 is WGS84/Unprojected #3395 is WGS84/Mercator. #4283 is Australia
        crs = {"type": "name", "properties": {"name": srs_name}}
        geometries = []
        member_elems = geom.iterchildren(tag=surface_member_tag)
        for m in member_elems:
            member = gml_extract_geom_to_geojson(m, recursion=recursion+1,
                                                 parent_srs=srs_name)
            geometries.append(member)
        return {"type": "GeometryCollection", "geometries": geometries, "dims": srs_dims, "crs": crs}
    if geom.tag == MultiSurface:
        srs_dims = int(geom.get('srsDimension', 2))
        srs_name = geom.get('srsName', default_srs) #4326 is WGS84/Unprojected #3395 is WGS84/Mercator. #4283 is Australia
        crs = {"type": "name", "properties": {"name": srs_name}}
        coords = []
        member_elems = geom.iterchildren(tag=surface_member_tag)
        for m in member_elems:
            member = gml_extract_geom_to_geojson(m, recursion=recursion+1,
                                                 parent_srs=srs_name)
            if member['type'] == "Polygon":
                coords.append(member['coordinates'])
            elif member['type'] == "MultiPolygon":
                coords.extend(member['coordinates'])
            else:
                raise ValueError(
                    "Multipolygon cannot have a member of type {}".format(member['type']))
        return {"type": "MultiPolygon", "coordinates": coords, "dims": srs_dims, "crs": crs}
    elif geom.tag == Polygon:
        def extract_poly_coords(node, dims=2, srs=None):
            """

            :param elem:
            :type elem: etree._Element
            :return:
            """
            nonlocal LinearRing
            nonlocal posList, pos
            flip_xy = True
            if srs and ("EPSG:3857" in srs or "EPSG:6.9:3857" in srs):
                flip_xy = False
            elem = next(node.iterchildren())  # type: etree._Element
            if elem.tag == LinearRing:
                coords = []
                pos_list_elems = list(elem.iterchildren(tag=posList))
                if len(pos_list_elems) > 0:
                    pos_list = pos_list_elems[0]
                    pos_list = str(pos_list.text).split()
                else:
                    pos_list = []
                    pos_elems = list(elem.iterchildren(tag=pos))
                    for pos_elem in pos_elems:
                        pos_members = str(pos_elem.text).split()
                        if len(pos_members) != dims:
                            raise ValueError(
                                "Dims = {:s} but pos has a different number of dimensions."\
                                    .format(str(dims)))
                        pos_list.extend(pos_members)
                if dims == 2:
                    if flip_xy:
                        for x, y in chunks(pos_list, 2):
                            coords.append((float(y), float(x)))
                    else:
                        for x, y in chunks(pos_list, 2):
                            coords.append((float(x), float(y)))
                elif dims == 3:
                    if flip_xy:
                        for x, y, z in chunks(pos_list, 3):
                            coords.append((float(y), float(x), float(z)))
                    else:
                        for x, y, z in chunks(pos_list, 3):
                            coords.append((float(x), float(y), float(z)))
                elif dims == 4:
                    if flip_xy:
                        for x, y, z, w in chunks(pos_list, 4):
                            coords.append(
                                (float(y), float(x), float(z), float(w)))
                    else:
                        for x, y, z, w in chunks(pos_list, 4):
                            coords.append(
                                (float(x), float(y), float(z), float(w)))
                return coords
            else:
                raise NotImplementedError(
                    "Poly geom type {} is not implemented.".format(elem.tag))
        poly_dict = {'exterior': None, 'interior': []}
        srs_dims = int(geom.get('srsDimension', 2))
        srs_name = geom.get('srsName', default_srs)  # 4326 is WGS84/Unprojected #3395 is WGS84/Mercator. #4283 is Australia
        crs = {"type": "name", "properties": {"name": srs_name}}
        exterior_elems = list(geom.iterchildren(tag=exterior_tag))
        if len(exterior_elems) > 0:
            exterior = exterior_elems[0]
            poly_dict['exterior'] = extract_poly_coords(exterior, dims=srs_dims, srs=srs_name)
        interior_elems = list(geom.iterchildren(tag=interior_tag))
        for interior_elem in interior_elems:
            interior = extract_poly_coords(interior_elem, dims=srs_dims, srs=srs_name)
            poly_dict['interior'].append(interior)
        coords = []
        if poly_dict['exterior']:
            coords.append(poly_dict['exterior'])
        else:
            coords.append([])
        coords.extend(poly_dict['interior'])
        return {"type": "Polygon", "crs": crs, "dims": srs_dims, "coordinates": coords}

    else:
        raise NotImplementedError(
            "Don't know how to convert geom type: {}".format(geom.tag))