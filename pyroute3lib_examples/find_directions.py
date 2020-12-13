from pyroutelib3 import Router # Import the router
router = Router("car") # Initialise it

print ("Finding")
start = router.findNode(51.53495526869262, -0.20454431828209635) # Find start and end nodes
end = router.findNode(51.5305246465236, -0.18548599498011692)

status, route = router.doRoute(start, end) # Find the route - a list of OSM nodes

if status == 'success':
    routeLatLons = list(map(router.nodeLatLon, route)) # Get actual route coordinates

print (routeLatLons)

