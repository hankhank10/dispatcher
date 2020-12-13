from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.units import miles
geolocator = Nominatim(user_agent="street_address_finder_hank")

from pyroutelib3 import Router # Import the router
router = Router("car") # Initialise it

import random

def lookup_by_address(address):
    location = geolocator.geocode(address)
    return location

def lookup_by_coordinates(latitude, longitude):
    lat_lon_string = str(latitude) + ", " + str(longitude)

    #location = geolocator.reverse("51.53707744842644, -0.20337486412392483")
    location = geolocator.reverse(lat_lon_string)

    return location

def find_directions(start_latitude, start_longitude, end_latitude, end_longitude):
    start_coords = router.findNode(start_latitude, start_longitude) # Find start and end nodes
    end_coords = router.findNode(end_latitude, end_longitude)
    
    status, route = router.doRoute(start_coords, end_coords) # Find the route - a list of OSM nodes

    if status == 'success':
        route_lat_lons = list(map(router.nodeLatLon, route)) # Get actual route coordinates
        return route_lat_lons

    return 'failure'
    
def find_distance(start_latitude, start_longitude, end_latitude, end_longitude):
    start_coords = (start_latitude, start_longitude)
    end_coords = (end_latitude, end_longitude)

    miles = geodesic(start_coords, end_coords).miles
    return miles

def time_to_travel(miles_to_travel, miles_per_hour=15):
    seconds_per_hour = 60*60
    miles_per_second = miles_per_hour / seconds_per_hour
    seconds_taken = miles_to_travel / miles_per_second
    return seconds_taken

def generate_random_coord(centrepoint_latitude, centrepoint_longitude, max_miles_away):

    mile_in_degree_of_latitude = 1 / 69
    mile_in_degree_of_longitude = 1 / 54.6

    max_latitude_away = max_miles_away * mile_in_degree_of_latitude
    max_longitude_away = max_miles_away * mile_in_degree_of_longitude

    conversion_factor = 1000000000000

    max_latitude_away_converted = int(max_latitude_away * conversion_factor)
    max_longitude_away_converted = int(max_longitude_away * conversion_factor)

    current_latitude_converted = int(centrepoint_latitude * conversion_factor)
    current_longitude_converted = int(centrepoint_longitude * conversion_factor)
    
    latitude_difference_converted = random.randint(1, max_latitude_away_converted)
    longitude_difference_converted = random.randint(1, max_longitude_away_converted)

    if random.randint(0,1) == 1:
        latitude_difference_converted = latitude_difference_converted * -1
    
    if random.randint(0,1) == 1:
        longitude_difference_converted = longitude_difference_converted * -1

    new_latitude_converted = current_latitude_converted + latitude_difference_converted
    new_longitude_converted = current_longitude_converted + longitude_difference_converted

    new_latitude = new_latitude_converted / conversion_factor
    new_longitude = new_longitude_converted / conversion_factor
    
    return new_latitude, new_longitude


#address = input ("Enter address> ")
address = "3628 sw 309th street 98023"
location = lookup_by_address(address)
print ("Location: ", location.latitude, location.longitude)

random_latitude, random_longitude = generate_random_coord(location.latitude, location.longitude, 1)
print ("Random location: ", str(random_latitude), ",", str(random_longitude))

random_name = lookup_by_coordinates (random_latitude, random_longitude)
print (random_name.address)
