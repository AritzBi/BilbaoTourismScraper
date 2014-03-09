from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
from demo.items import BuildingItem

class PatrimonioBilbaoTurismoSpider(Spider):
	BASE='http://www.bilbaoturismo.net'
	name='bTurismoPatrimonio_spider_es'
	allowed_domains=['bilbaoturismo.net']
	start_urls=['http://www.bilbaoturismo.net/BilbaoTurismo/es/edificios-emblematicos']

	def parse(self,response):
		sel=Selector(response)
		links=sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[1]/section/ul/li/a/@href").extract()
		for link in links:
			url=''.join([self.BASE,link])
			yield Request(url)
		#Para diferenciar entre lso diferentes tipos de links que hay 
		#Es solo para los edificios emblematicos del ensanche.
		edificiosEmblematicos=sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[1]/section/ul/li[3]/ul/li[2]")
		sectionMonumentos=sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[3]")
		esMonumento=sel.xpath("//*[@id='botonMostrarMapa']")
		if len(sectionMonumentos)>0:
			otherURLS = sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[3]/div/p/a[contains(.,'>>>')]/@href").extract()
			if len(otherURLS)>0:
				url=''.join([self.BASE,otherURLS.pop()])
				yield Request(url)
			yield Request(response.url,callback=self.parse_list_monuments,dont_filter=True)
		elif len(edificiosEmblematicos)>0:
			link=edificiosEmblematicos.xpath("a/@href").extract().pop()
			url=''.join([self.BASE,link])
			yield Request(url)
		elif len(esMonumento)>0:
			yield Request(response.url,callback=self.parse_monuments,dont_filter=True)

	def parse_list_monuments (self,response):
		sel = Selector(response)
		listings = sel.xpath('//section[@class="column x-image"]')
		links = []
		for listing in listings:
			link=listing.xpath('a/@href').extract()[0]
			links.append(link)
		for link in links:
			yield Request(self.BASE+str(link),callback=self.parse_monuments)

	def parse_monuments(self,response):
		sel=Selector(response)
		monument=sel.xpath('//div[@class="col-50 content-desc"]')
		title=monument.xpath("h2[@class='big sec-color']/text()").extract()
		summary=''.join(monument.xpath("div[@id='idContentScroll']/span/p/text()").extract())
		address=monument.xpath("span/text()").re(r'[\w\s,-\/]*\s48\d{3}\s*\w*')
		informationLink=monument.xpath("div[@id='idContentScroll']/span/a/@href").extract()
		monumentoReligioso=sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[1]/section/ul/li/a[@class='sec-bg'][contains(.,'Monumentos religiosos')]").extract()
		if monumentoReligioso:
			category="Monumento Religioso"
		else:
			category="Monumento Historico"
		item=BuildingItem()
		if len(title)>0:
			item['name']=title.pop()
		else:
			item['name']=''
		if len(summary)>0:
			item['description']=summary
		else:
			item['description']=''
		if len(address)>0:
			item['address']=address.pop().strip()
		else:
			item['address']=''
		if len(informationLink)>0:
			item['informationLink']=informationLink.pop()
		else:
			item['informationLink']=response.url
		item['category']=category

		return item

