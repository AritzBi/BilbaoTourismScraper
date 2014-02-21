from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector

class RestaurantesSpider(Spider):
	BASE='http://turismo.euskadi.net'
	name='restaurantes_spider'
	allowed_domains=['turismo.euskadi.net']
	start_urls=['http://turismo.euskadi.net/x65-15634x/es/s12PortalWar/buscadoresJSP/buscadorB1.jsp?r01kLang=es&marks=4&restorationType=R']

	def parse(self,response):
		sel = Selector(response)
		otherURLS = sel.xpath('//*[@id="containerConRutas"]/div[3]/div/div/div/div/div[3]/div/ul')
		relativeURLS=otherURLS.xpath("li[@class='r01NavBarItem r01NavBarIntermediateItem']/a/@href").extract()
		#EL ultimo de la lista tiene una clase diferente.
		lastRelativeURL=otherURLS.xpath("li[@class='r01NavBarItem']/a/@href").extract()
		if len(lastRelativeURL)>0:
			relativeURLS.append(lastRelativeURL.pop())
		moreLinksPage=otherURLS.xpath("li[@class='r01NavBarCtrlItem r01NavBarNextBlock']/a/@href").extract()
		for relativeLink in relativeURLS:
			url=self.BASE+relativeLink
			print url
			yield Request(url,callback=self.parse_restaurants_links)

	def parse_restaurants_links(self,response):
