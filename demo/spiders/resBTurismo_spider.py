from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
import datetime


class RestauranteBilbaoTurismoSpider(Spider):
	BASE='http://www.bilbaoturismo.net'
	name='bTurismoRes_spider'
	allowed_domains=['bilbaoturismo.net']
	start_urls=['http://www.bilbaoturismo.net/BilbaoTurismo/es/buscador-de-pintxos?zona=1361356724680,1361356724448,1361356724652,1361356724659,1361356724666,1361356724673,1361356724467,1361356724481&tipologia=']

	def parse(self,response):
		sel = Selector(response)
		otherURLS = sel.xpath("//*[@id='gastronomy-content']/section[2]/div/section[2]/div/section[2]/div/p/a[contains(.,'>>>')]/@href").extract()
		if len(otherURLS)>0:
			url=''.join(self.BASE+otherURLS.pop())
			yield Request(url)
		yield Request(response.url,callback=self.parse_restaurants_links,dont_filter=True)
	def parse_restaurants_links(self, response):
		sel=Selector(response)
		restaurants= sel.xpath("//*[@id='gastronomy-content']/section[2]/div/section[2]/div/section[2]/section/section/a/@href").extract()
		print restaurants