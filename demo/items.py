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
	date=Field()
	hour=Field()
	location=Field()
	category=Field()
	
class BilbaoItem(Item):
	title=Field()
	startDate=Field()
	endDate=Field()
	summary=Field()
	location=Field()
	nearestMetro=Field()
	postalCode=Field()
	city=Field()
	hour=Field()
class Item(Item):
	title=Field()
	link=Field()
	description=Field()
