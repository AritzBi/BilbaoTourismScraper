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
	title_en=Field()
	title_eu=Field()
	description=Field()
	description_en=Field()
	description_eu=Field()
	locationName=Field()
	locationAddress=Field()
	locationWebsite=Field()
	locationEmail=Field()
	locationTelephone=Field()
	lat=Field()
	lon=Field()
	lowPrice=Field()
	highPrice=Field()
	rangePrices=Field()
	startDate=Field()
	endDate=Field()
	startHour=Field()
	endHour=Field()
	informationLink=Field()
	category=Field()
	category_en=Field()
	category_eu=Field()
	moreInformation=Field()
	moreInformation_en=Field()
	moreInformation_eu=Field()
	image_urls = Field()
	image_paths= Field()
	
class RestaurantItem(Item):
	name=Field()
	category=Field()
	category_en=Field()
	category_eu=Field()
	address=Field()
	information=Field()
	information_en=Field()
	information_eu=Field()
	telephone=Field()
	timetable=Field()
	timetable_en=Field()
	timetable_eu=Field()
	michelin=Field()
	repsol=Field()
	email=Field()
	informationLink=Field()
	originLink=Field()
	description=Field()
	description_en=Field()
	description_eu=Field()
	image_urls = Field()
	image_paths= Field()

class BuildingItem(Item):
	name=Field()
	name_en=Field()
	name_eu=Field()
	category=Field()
	category_en=Field()
	category_eu=Field()
	address=Field()
	description=Field()
	description_en=Field()
	description_eu=Field()
	informationLink=Field()
	informationLink_en=Field()
	informationLink_eu=Field()
	image_urls = Field()
	image_paths= Field()
class Item(Item):
	title=Field()
	link=Field()
	description=Field()
