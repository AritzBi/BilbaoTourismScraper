# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DemoItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class EventItem(Item):
	title=Field()
	description=Field()
	locationName=Field()
	locationAddress=Field()
	locationWebsite=Field()
	locationEmail=Field()
	locationTelephone=Field()
	lat=Field()
	lon=Field()
	priceAnticipada=Field()
	priceTaquilla=Field()
	rangePrices=Field()
	startDate=Field()
	endDate=Field()
	startHour=Field()
	endHour=Field()
	informationLink=Field()
	category=Field()
	observations=Field()
	
class RestaurantItem(Item):
	name=Field()
	category=Field()
	address=Field()
	information=Field()
	telephone=Field()
	timetable=Field()
	michelin=Field()
	repsol=Field()
	email=Field()
	informationLink=Field()
	description=Field()

class BuildingItem(Item):
	name=Field()
	category=Field()
	address=Field()
	description=Field()
	informationLink=Field()
class Item(Item):
	title=Field()
	link=Field()
	description=Field()
