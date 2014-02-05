from scrapy.spider import Spider 
from scrapy.selector import Selector
from demo.items import EventItem

class DemoSpider(Spider):
	name="antzoki_spider"
	allowed_domains=["kafeantzokia.com"]
	start_urls=["http://www.kafeantzokia.com/web/agenda?lang=es"]

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath('//tbody/tr')
		items = []
		for site in sites:
			#The type of item is defined.
			item = EventItem()
			item['title'] = site.xpath("td[@headers='el_title']/a/text()").extract()
			#item['title'] = site.xpath("/td[@headers='el_title']/a/text()").extract()
			item['date'] = site.xpath("td[@headers='el_date']/strong/text()").extract()
			item['hour'] = site.xpath("td[@headers='el_date']/text()").extract()
			item['location'] = site.xpath("td[@headers='el_location']/a/text()").extract()
			item['category'] = site.xpath("td[@headers='el_category']/a/text()").extract()
			items.append(item)
		return items