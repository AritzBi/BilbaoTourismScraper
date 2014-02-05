from pygeocoder import Geocoder

results=Geocoder.geocode("Kafe Antzokia, Bilbao")
coordinates=results[0].coordinates
#coordinates=coordinates.split(',')
print coordinates[0]
print coordinates[1]
print results[0].city
print results[0].postal_code
#print results[0]