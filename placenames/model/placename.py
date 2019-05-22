# -*- coding: utf-8 -*-
from flask import render_template, Response
from rdflib import Graph, URIRef, RDF, RDFS, XSD, OWL, Namespace, Literal, BNode
import placenames._conf as conf
from psycopg2 import sql
import json
import decimal
from pyldapi import Renderer, View


class Placename(Renderer):
    """
    This class represents an Address and methods in this class allow an Address to be loaded from the GNAF database
    and to be exported in a number of formats including RDF, according to the 'GNAF Ontology' and an
    expression of the Dublin Core ontology, HTML, XML in the form according to the AS4590 XML schema.
    """

    def __init__(self, request, uri):
        views = {
            'pn': View(
                'Plane Names View',
                'This view is the standard view delivered by the Place Names dataset in accordance with the '
                'Place Names Profile',
                ['text/html', 'text/turtle', 'application/ld+json'],
                'text/html'
            )
        }

        super(Placename, self).__init__(request, uri, views, 'pn', None)
        self.id = 'not_needed_in_testing'  # get this from the request object's URI

        # for place in conf.db_select('SELECT ...'):
        #     pass

        '''
        "ID","AUTH_ID","NAME","FEATURE","CATEGORY","GROUP","LATITUDE","LONGITUDE","AUTHORITY","SUPPLY_DATE","geom"
        '''

        '''
        
        "WA_100039525","100039525","Willow Well","BORE","WATER POINT","HYDROLOGY","-27.80843","118.47919","WA","2018-02-19 02:57:38","0101000020BB1000007FA4880CAB9E5D40F41ABB44F5CE3BC0"
        "WA_100040525","100040525","Wyening Mission","MISSION","PLACE OF WORSHIP","CULTURE","-31.16154","116.5423","WA","2018-02-19 02:57:52","0101000020BB100000BB270F0BB5225D40EFFE78AF5A293FC0"
        '''
        dummy_instance = {
            'id': "WA_100156123",
            'auth_id': "100156123",
            'name': "Dummy Well",
            'feature': "BORE",
            'category': "WATER POINT",
            'group': "HYDROLOGY",
            'latitude': "-25.9126",
            'longitude': "116.75556",
            'authority': "WA",
            'supply_date': "2018-02-19 02:57:40",
            'geom': "0101000020BB1000009C8A54185B305D4061545227A0E939C0",
            'pronunciation': 'dummee wel'  # not in current data
        }

        gazetteers = {
            'Antarctica': {
                'label': 'Australian Antarctica Gazetteer',
                'uri_id': 'aag'
            },
            'WA': {
                'label': 'Western Australia\'s Place Names Gazetteer',
                'uri_id': 'wa'
            }
        }

        naming_authorities = {
            'ACT': {
                'label': 'Australian Capital Territory',
                'uri_id': 'act'
            },
            'AAD': {
                'label': 'Australian Antarctic Division',
                'uri_id': 'aad'
            },
            'WA': {
                'label': 'Western Australian Government',
                'uri_id': 'wa'
            }
        }

        self.hasName = {
            'uri': 'http://linked.data.gov.au/def/placename/hasName',
            'label': 'has name',
            'comment': 'The Entity has a name (label) which is a text sting.',
            'value': dummy_instance.get('name')
        }
        self.register = {
            'label': gazetteers.get(dummy_instance.get('authority'))['label'],
            'uri': conf.GAZETTEER_INSTANCE_URI_STEM + gazetteers.get(dummy_instance.get('authority'))['uri_id']
        }
        self.wasNamedBy = {
            'label': naming_authorities.get(dummy_instance.get('authority'))['label'],
            'uri': conf.JURISDICTION_INSTANCE_URI_STEM + naming_authorities.get(dummy_instance.get('authority'))['uri_id']
        }
        self.hasNameFormality = {
            'label': 'Official',
            'uri': 'http://linked.data.gov.au/def/placenames/nameFormality/Official'
        }
        self.hasPronunciation = dummy_instance.get('pronunciation')

    def render(self):
        if self.view == 'alternates':
            return self._render_alternates_view()
        elif self.format in ['text/turtle', 'application/ld+json']:
            return self.export_rdf()
        else:  # default is HTML response: self.format == 'text/html':
            return self.export_html()

    def export_html(self):
        return Response(
            render_template(
                'placename.html',
                id="TEST",
                hasName=self.hasName,
                hasPronunciation=self.hasPronunciation,
                register=self.register,
                wasNamedBy=self.wasNamedBy,
                hasNameFormality=self.hasNameFormality
                # schemaorg=self.export_schemaorg()
            ),
            status=200,
            mimetype='text/html'
        )
        # if we had multiple views, here we would handle a request for an illegal view
        # return NotImplementedError("HTML representation of View '{}' is not implemented.".format(view))

    def export_rdf(self):
        g = Graph()

        PN = Namespace('http://linked.data.gov.au/def/placename/')
        g.bind('pn', PN)

        me = URIRef(self.uri)

        g.add((me, RDF.type, URIRef('http://linked.data.gov.au/def/placename/PlaceName')))  # PN.PlaceName))
        g.add((me, PN.hasName, Literal(self.hasName['value'], datatype=XSD.string)))

        if self.format == 'text/turtle':
            return Response(
                g.serialize(format='turtle'),
                mimetype='text/turtle'
            )
        else:  # JSON-LD
            return Response(
                g.serialize(format='json-ld'),
                mimetype='application/ld+json'
            )

    def export_schemaorg(self):
        data = {
            '@context': 'http://schema.org',
            '@type': 'Place',
            'address': {
                '@type': 'PostalAddress',
                'streetAddress': self.address_string.split(',')[0],
                'addressLocality': self.locality_name,
                'addressRegion': self.state_prefLabel,
                'postalCode': self.postcode,
                'addressCountry': 'AU'
            },
            'geo': {
                '@type': 'GeoCoordinates',
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'name': 'Geocoded Address ' + self.id
        }

        return json.dumps(data, cls=DecimalEncoder)


if __name__ == '__main__':
    a = Address('GANSW703902211', focus=True)
    print(a.export_rdf().decode('utf-8'))

# has alias for which it can't get address subclass: GAACT715069724. Alias is GAACT718348352
# GAACT718348352 has subclass UnknownVillaAddress
