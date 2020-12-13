from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="street_address_finder_hank")

lat = 51.53707744842644
lon = -0.20337486412392483
lat_lon_string = str(lat) + ", " + str(lon)
print(lat_lon_string)

#location = geolocator.reverse("51.53707744842644, -0.20337486412392483")
location = geolocator.reverse(lat_lon_string)


print(location.address)

print((location.latitude, location.longitude))

print(location.raw)
