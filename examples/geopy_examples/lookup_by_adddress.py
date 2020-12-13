from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="street_address_finder_hank")

print("")
address = input("What address?")

location = geolocator.geocode(address)

print(location.address)
print("")

print((location.latitude, location.longitude))
print("")

print(location.raw)