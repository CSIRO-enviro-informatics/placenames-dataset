from flask import Blueprint, request, redirect, url_for, Response, render_template
from placenames.model.placename import Placename
from pyldapi import RegisterRenderer

routes = Blueprint('controller', __name__)


@routes.route('/', strict_slashes=True)
def home():
    return render_template('home.html')


@routes.route('/placenames/')
def placenames():
    # get the total register count from the XML API
    try:
        # MAGIC NUMBER DUMMY COUNT
        # no_of_items = 42

        # page = request.values.get('page') if request.values.get('page') is not None else 1
        # per_page = request.values.get('per_page') if request.values.get('per_page') is not None else 3
        items = [
            ('http://fake.com/1', 'Fake 1'),
            'http://fake.com/2',
            ('http://fake.com/3', 'Fake 3'),
            ('http://fake.com/4', 'Fake 4'),
            ('http://fake.com/5', 'Fake 5'),
            ('http://fake.com/6', 'Fake 6'),
        ]
    except Exception as e:
        print(e)
        return Response('The Samples Register is offline', mimetype='text/plain', status=500)

    return RegisterRenderer(
        request,
        request.url,
        'Place Names Register',
        'A register of Place Names',
        items,
        ['http://linked.data.gov.au/def/placenames/PlaceName'],
        len(items)
    ).render()


@routes.route('/placename/<string:placename_id>')
def placename(placename_id):
    pn = Placename(request, request.base_url)
    return pn.render()
