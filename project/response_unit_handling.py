from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import db
from . import mapfunctions

from .models import ResponseUnit
from .models import Path
from .models import Waypoint

from . import pathfinding_handling

import datetime

response_unit_handling = Blueprint('response_unit_handling', __name__)


@response_unit_handling.route ("/gamelogic/create_new_response_unit")
def create_new_response_unit():

    start_point_tuple = (51.50984266384934, -0.12466092828771125)

    new_response_unit = ResponseUnit(
        last_known_latitude = start_point_tuple[0],
        last_known_longitude = start_point_tuple[1],
        status = "available",
        current_path = 0
    )

    db.session.add(new_response_unit)
    db.session.commit()

    return str(new_response_unit.id)


@response_unit_handling.route("/json/view_response_unit/<response_unit_id>")
def json_response_unit(response_unit_id):
    response_unit = ResponseUnit.query.filter_by(id = response_unit_id).first_or_404()

    output_dictionary = {}
    output_dictionary["id"] = response_unit_id
    output_dictionary["last_known_latitude"] = response_unit.last_known_latitude
    output_dictionary["last_known_longitude"] = response_unit.last_known_longitude
    output_dictionary["status"] = response_unit.status
    output_dictionary["current_path"] = response_unit.current_path
    output_dictionary["google_maps_link"] = "https://www.google.co.uk/maps/place/" + str(response_unit.last_known_latitude) + "," + str(response_unit.last_known_longitude)

    return jsonify(output_dictionary)


def assign_response_unit_to_callout(response_unit_id, callout_id):
    # Get the response unit from the database and work out the start point
    response_unit = ResponseUnit.query.filter_by(id = response_unit_id).first()
    start_point_tuple = (response_unit.last_known_latitude, response_unit.last_known_longitude)

    # Create the path
    new_path_id = pathfinding_handling.create_new_path(start_point_tuple, callout_id)

    # Set the response unit to move along that path
    response_unit.current_path = new_path_id
    response_unit.status = "en route"
    db.session.commit()

    # Get the callout ID and set it as "responding"
    ### DO THIS LATER

    return new_path_id


@response_unit_handling.route ("/assign_response_unit/<response_unit_id>/to_callout/<callout_id>")
def assign_response_unit_to_callout_endpoint(response_unit_id, callout_id):
    new_path_id = assign_response_unit_to_callout(response_unit_id, callout_id)

    return "Response unit " + str(response_unit_id) + " assigned to callout " + str(callout_id) + " with path " + str(new_path_id)


@response_unit_handling.route ("/gamelogic/update_unit_location/<response_unit_id>")
def update_location(response_unit_id):
    response_unit = ResponseUnit.query.filter_by(id = response_unit_id).first()

    if response_unit.current_path > 0:

        last_waypoint = Waypoint.query.filter(
            Waypoint.member_of_path_id == response_unit.current_path, 
            Waypoint.time_due_to_arrive < datetime.datetime.utcnow()
            ).order_by(Waypoint.time_due_to_arrive.desc()).first()

        response_unit.last_known_latitude = last_waypoint.latitude
        response_unit.last_known_longitude = last_waypoint.longitude

        if last_waypoint.is_last_point_in_path == True:
            response_unit.current_path = 0
            response_unit.status = "on scene"
            # ALSO MARK INCIDENT AS RESPONDING
            
        db.session.commit()

    return redirect(url_for('response_unit_handling.json_response_unit', response_unit_id = response_unit_id))
