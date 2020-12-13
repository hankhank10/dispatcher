from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import db
from . import mapfunctions

from .models import Callout

callout_handling = Blueprint('callout_handling', __name__)

# Global variables
centrepoint_tuple = (51.510403379154475, -0.13009936801710234)
max_miles_away_from_centrepoint = 2


def create_new_callout():
    valid_location = False
    
    while valid_location == False:
        print ("Trying to generate address")

        # Generate a random latitude and longitude
        new_latitude, new_longitude = mapfunctions.generate_random_coord(centrepoint_tuple[0], centrepoint_tuple[1], max_miles_away_from_centrepoint)

        # Get the address based on that latitude and longitude
        location_address = mapfunctions.lookup_by_coordinates(new_latitude, new_longitude).address

        # Now RESOLVE for the latitude and longitude based on that location
        exact_location = mapfunctions.lookup_by_address (location_address)

        if exact_location == None:
            print ("Invalid... trying again...")
        else:
            valid_location = True

    new_callout = Callout(
        latitude = exact_location.latitude,
        longitude = exact_location.longitude,
        location_address = location_address,
        status = "pendingf"
        )

    db.session.add(new_callout)
    db.session.commit()

    return new_callout.id


@callout_handling.route ("/gamelogic/create_new_callout")
def new_callout_endpoint():
    
    new_callout_id = create_new_callout()
    #return str(new_callout_id)s

    return redirect(url_for('callout_handling.json_view_callout', callout_id = new_callout_id))


@callout_handling.route ("/json/view_callout/<callout_id>")
def json_view_callout(callout_id):

    callout = Callout.query.filter_by(id = callout_id).first_or_404()
    
    output_dictionary = {}
    output_dictionary["id"] = callout_id
    output_dictionary["latitude"] = callout.latitude
    output_dictionary["longitude"] = callout.longitude
    output_dictionary["address"] = callout.location_address
    output_dictionary["google_maps_link"] = "https://www.google.co.uk/maps/place/" + str(callout.latitude) + "," + str(callout.longitude)
    
    return jsonify(output_dictionary)


