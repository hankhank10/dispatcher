from . import db
from datetime import datetime, timedelta


class Callout(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_address = db.Column(db.String)
    status = db.Column(db.String)   # hidden, pending, allocated, on scene, resolved


class ResponseUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy

    # Where the unit is
    last_known_latitude = db.Column(db.Float)
    last_known_longitude = db.Column(db.Float)
    
    # What the unit is called
    shift_name = db.Column(db.String)
    unit_name = db.Column(db.String)
    
    @property
    def callsign (self):
        return self.shift_name + "/" + self.unit_name


    # What the unit is doing
    status = db.Column(db.String)   # hidden, available, en route, on scene, inactive
    current_path = db.Column(db.Integer)
    responding_to_callout = db.Column(db.Integer)
    
    

class Path(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    to_callout = db.Column(db.Integer)


class Waypoint(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    member_of_path_id = db.Column(db.Integer)
    number_within_path = db.Column(db.Integer)
    is_last_point_in_path = db.Column(db.Boolean)
    time_due_to_arrive = db.Column(db.DateTime)