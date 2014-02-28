from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
import datetime

#Restaurantes
#TODO: Si no hay URL poner response.url
#Posible: Metro cercano
class RestaurantesBilbaoTurismoSpider(Spider):
	BASE='http://www.bilbaoturismo.net'
	name='bTurismoRestaurantes_spider'
	allowed_domains=['bilbaoturismo.net']
	start_urls=['http://www.bilbaoturismo.net/BilbaoTurismo/es/restaurantes?zona=1361356724448,1361356724460,1361356724474,1361356724467,1361356724488,1361356724481&tipologia=']
	def parse(self,response):
		sel = Selector(response)
		otherURLS = sel.xpath("//*[@id='gastronomy-content']/section[2]/div/section/div/section[2]/div/p/a[contains(.,'>>>')]/@href").extract()
		if len(otherURLS)>0:
			url=''.join([self.BASE,otherURLS.pop()])
			yield Request(url)
		yield Request(response.url,callback=self.parse_restaurants_links,dont_filter=True)
	def parse_restaurants_links(self, response):
		sel=Selector(response)
		listings = sel.xpath("//*[@id='gastronomy-content']/section[2]/div/section/div/section[2]/section/section")
		links = []
		for listing in listings:
			link=listing.xpath('a/@href').extract()[0]
			links.append(link)
		for link in links:
			yield Request(self.BASE+str(link),callback=self.parse_restaurants)
	def parse_restaurants(self,response):
		sel=Selector(response)
		name=sel.xpath("//*[@id='sectionDetalle']/div[1]/h2/text()").extract()
		address=sel.xpath("//*[@id='sectionDetalle']/div[1]/span")
		streetAddress=address.xpath("span[@itemprop='streetAddress']/text()").extract()
		postalCode=address.xpath("span[@itemprop='postalCode']/text()").extract()
		addressLocality=address.xpath("span[@itemprop='addressLocality']/text()").extract()
		telephone=address.xpath("span[@itemprop='telephone']/text()").extract()
		email=address.xpath("span[@itemprop='email']/text()").extract()
		descriptionpath=sel.xpath("//*[@id='idContentScroll']")
		description=descriptionpath.xpath("span[@itemprop='description']/p/text()").extract()
		informationLink=descriptionpath.xpath("span/a/@href").extract()
		categoryPath=sel.xpath("//*[@id='gastronomy-content']/section[2]/div/section[1]/section/div/ul/li[2]/p[2]")
		category=categoryPath.xpath("a/strong/text()").extract()
		"""print name
		print addressLocality
		print streetAddress
		print postalCode
		print telephone
		print email
		print description
		print informationLink
		print category"""