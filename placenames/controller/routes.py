from flask import Blueprint, request, redirect, url_for, Response, render_template
from placenames.model.placename import Placename
from pyldapi import View

routes = Blueprint('controller', __name__)


@routes.route('/', strict_slashes=True)
def home():
    return render_template('home.html')


@routes.route('/place/')
def placenames():
    return 'register of Places'


@routes.route('/placename/<string:placename_id>')
def placename(placename_id):
    pn = Placename(request, request.base_url)
    return pn.render()
