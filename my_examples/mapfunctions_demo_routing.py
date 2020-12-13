from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.units import miles
geolocator = Nominatim(user_agent="street_address_finder_hank")

from pyroutelib3 import Router # Import the router
router = Router("car") # Initialise it

def lookup_by_address(address):
    location = geolocator.geocode(address)
    return location

def lookup_by_coordinates(latitude, longitude):
    location = geolocator.reverse(latitude, longitude)
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


#start_address = input ("Start addreess> ")
start_address = "3268 SW 309th Street 98023"
start_location = lookup_by_address(start_address)
print ("Start:", start_location.latitude, start_location.longitude)

#end_address = input ("End addreess> ")
end_address = "1656 SW Dash Point Rd 98023"
end_location = lookup_by_address(end_address)
print ("End:", end_location.latitude, end_location.longitude)

distance_between = find_distance(start_location.latitude, start_location.longitude, end_location.latitude, end_location.longitude)
print ("Total distance: ", distance_between, "miles")

print ("")
route_lat_lons = find_directions (start_location.latitude, start_location.longitude, end_location.latitude, end_location.longitude)
if route_lat_lons == 'failure':
    print ("Route could not be found")
else:
    # append end point
    route_lat_lons.append((end_location.latitude, end_location.longitude))

    #a=0
    #for waypoint in route_lat_lons:
    #    print ("Waypoint", a, ":", waypoint[0], ",", waypoint[1])
    #    a = a + 1
    
    total_seconds = 0
    number_of_waypoints = len(route_lat_lons)-1
    for i in range(number_of_waypoints+1):
        print ("Waypoint",str(i), "of", str(number_of_waypoints), ":", route_lat_lons[i][0], route_lat_lons[i][1])
        if i < number_of_waypoints:
            distance_to_next = find_distance (route_lat_lons[i][0], route_lat_lons[i][1], route_lat_lons[i+1][0], route_lat_lons[i+1][1])
            seconds = time_to_travel(distance_to_next)
            total_seconds = total_seconds + seconds

            print (str(distance_to_next), "mile gap, which would take", str(seconds), "seconds")

    print (str(total_seconds), "total seconds")

