from flask import Blueprint, request, redirect, url_for, Response, render_template

routes = Blueprint('controller', __name__)


@routes.route('/', strict_slashes=True)
def home():
    return render_template('home.html')


@routes.route('/place/')
def places():
    return 'register of Places'


@routes.route('/place/<string:place_id>')
def place(place_id):
    return render_template('place.html', id=place_id)
