from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
import re

class RestaurantesSpider(Spider):
	BASE='http://turismo.euskadi.net'
	name='barespintxos_spider'
	allowed_domains=['servicios.elcorreo.com/']
	start_urls=['http://servicios.elcorreo.com/gastronomia/guia-bares/vizcaya-bilbao.html']

	def parse(self, response):
		sel=Selector(response)
		#print response.body

		listing=sel.xpath("//*[@id='contenido']/div/div/div/table[@id='colAB']/tr/td/div").extract()
		listing=sel.xpath("//*[@id='colAB']/tr[2]/td/table/tr/td[3]/h2[contains(.,'Pintxos')]/following-sibling::div").extract()
		print listing

