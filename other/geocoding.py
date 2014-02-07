from pygeocoder import Geocoder
from geopy import geocoders

"""results=Geocoder.geocode("Iglesia de la encarnacion")
coordinates=results[0].coordinates
#coordinates=coordinates.split(',')
print coordinates[0]
print coordinates[1]
print results[0].city
print results[0].postal_code
#print results[0]"""

g=geocoders.GoogleV3()
place, (lat, lng) = g.geocode("Alameda Urquijo 4 48008 Bilbao ")
print "%s: %.5f, %.5f" % (place, lat, lng)  

g=geocoders.GeoNames(None,'aritzbi',None)
place, (lat, lng) = g.geocode("Kafe Antzokia")
print "%s: %.5f, %.5f" % (place, lat, lng) 

#g=geocoders.Nominatim()
#place = g.geocode("Palacio Euskalduna",None,5)
#print "%s: %.5f, %.5f" % (place, lat, lng)  

g=geocoders.Bing('Ag1Y_zbKfJ-sIea_MXaCdtIgnnYojrBytkIc3Pa0L0JLeKcFBwitYBfJvyak5fhq',timeout=5)
place, (lat, lng) = g.geocode("Hesperia Bilbao", True, None, None)
print "%s: %.5f, %.5f" % (place, lat, lng)

#g=geocoders.YahooPlaceFinder('dj0yJmk9d0J4ak1RUWtSa1pVJmQ9WVdrOU5qWndRM1l6TXpBbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD02ZQ--','84555b31263138d53cabfb27c3b9dee5c3fb01c5',1,None)
#place, (lat, lng) = g.geocode("Palacio Euskalduna",True,None,0,False,False,None)
#print "%s: %.5f, %.5f" % (place, lat, lng)  

#43.263710, -2.928152