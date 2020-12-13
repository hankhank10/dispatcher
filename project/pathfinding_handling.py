from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import db
from . import mapfunctions

from .models import Callout
from .models import Path
from .models import Waypoint

import datetime

pathfinding_handling = Blueprint('pathfinding_handling', __name__)


def create_new_path(start_point_tuple, callout_id):
    
    # Define start point (manual for now)
    #start_point_tuple = (51.50984266384934, -0.12466092828771125)

    # Find end point
    callout = Callout.query.filter_by(id = callout_id).first_or_404()

    # Find path
    path_lat_lons = mapfunctions.find_directions(start_point_tuple[0], start_point_tuple[1], callout.latitude, callout.longitude)
    
    # Kick it out with a failure return it doesn't work, move on if it does
    if path_lat_lons == 'failure':
        print ("failure to find route")
        return ("failure")

    # Create the path record in the database
    new_path = Path(
        to_callout = callout_id
    )
    db.session.add(new_path)
    db.session.commit()

    # Set the start time as 30 seconds from now
    start_time = datetime.datetime.utcnow()
    start_time = start_time + datetime.timedelta (0, 5)
    
    # Calculate waypoints and timing
    total_seconds = 0
    number_of_waypoints = len(path_lat_lons)-1
    for i in range(number_of_waypoints+1):
        print ("Waypoint",str(i), "of", str(number_of_waypoints), ":", path_lat_lons[i][0], path_lat_lons[i][1])
        if i < number_of_waypoints:
            distance_to_next = mapfunctions.find_distance (path_lat_lons[i][0], path_lat_lons[i][1], path_lat_lons[i+1][0], path_lat_lons[i+1][1])
            seconds = mapfunctions.time_to_travel(distance_to_next)
            
            total_seconds = total_seconds + seconds
            arrival_utc_time = start_time + datetime.timedelta(0, total_seconds)

            if i == number_of_waypoints - 1:
                is_last_point_in_path = True
            else:
                is_last_point_in_path = False

            new_waypoint = Waypoint(
                latitude = path_lat_lons[i][0],
                longitude = path_lat_lons[i][1],
                member_of_path_id = new_path.id,
                number_within_path = i,
                time_due_to_arrive = arrival_utc_time,
                is_last_point_in_path = is_last_point_in_path
            )

            db.session.add(new_waypoint)
            db.session.commit()

            #print (str(distance_to_next), "mile gap, which would take", str(seconds), "seconds")

    print (str(total_seconds), "total seconds")
    return new_path.id


@pathfinding_handling.route ("/gamelogic/find_new_path_to_callout/<callout_id>")
def find_path_endpoint(callout_id):
    new_path_id = create_new_path(callout_id)
    
    return redirect(url_for('pathfinding_handling.html_view_path', path_id = new_path_id))


@pathfinding_handling.route ("/json/view_path/<path_id>")
def json_view_path(path_id):
    pass


@pathfinding_handling.route ("/view_path/<path_id>")
def html_view_path(path_id):

    waypoints = Waypoint.query.filter_by(member_of_path_id = path_id).all()
    return render_template("/simple/view_route.html", waypoints = waypoints)

