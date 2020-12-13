from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import db
from . import mapfunctions

from .models import Callout
from .models import ResponseUnit


main = Blueprint('main', __name__)


@main.route ("/")
def index_page():
    
    return render_template('/map.html')

@main.route ("/json/callout_data")
def json_callout_data():
    
    callouts = Callout.query.all()

    output_list = []

    for callout in callouts:
        output_dictionary = {
            'id': callout.id,
            'latitude': callout.latitude,
            'longitude': callout.longitude,
            'location_address': callout.location_address,
            'status': callout.status
        }
        output_list.append(output_dictionary)

    return jsonify(output_list)

