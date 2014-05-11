from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
from demo.items import BuildingItem

class MuseosBilbaoTurismoSpider(Spider):
	BASE='http://www.bilbaoturismo.net'
	name='museosBTurismo_spider'
	allowed_domains=['bilbaoturismo.net']
	start_urls=['http://www.bilbaoturismo.net/BilbaoTurismo/es/otros-museos']

	def parse(self,response):
		sel=Selector(response)
		#Guggenheim
		link1=sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[1]/section/ul/li[1]/a/@href").extract()
		yield Request(''.join([self.BASE,link1.pop()]),callback=self.parse_museums)
		#Bellas artes
		link2=sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[1]/section/ul/li[2]/a/@href").extract()
		yield Request(''.join([self.BASE,link2.pop()]),callback=self.parse_museums)
		#linkOtherMuseums=sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[1]/section/ul/li[3]/a/@href").extract()
		otherURLS = sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[3]/div/p/a[contains(.,'>>>')]/@href").extract()
		if len(otherURLS)>0:
			url=''.join([self.BASE,otherURLS.pop()])
			yield Request(url)
		yield Request(response.url,callback=self.parse_museums_links,dont_filter=True)
	def parse_museums_links(self,response):
		sel = Selector(response)
		listings = sel.xpath('//section[@class="column x-image"]')
		links = []
		for listing in listings:
			link=listing.xpath('a/@href').extract()[0]
			links.append(link)
		for link in links:
			yield Request(self.BASE+str(link),callback=self.parse_museums)


	def parse_museums(self, response):
		sel=Selector(response)
		museum=sel.xpath('//div[@class="col-50 content-desc"]')
		title=museum.xpath("h2[@class='big sec-color']/text()").extract()
		summary=''.join(museum.xpath("div[@id='idContentScroll']/span/p//text()").extract())
		address=museum.xpath("span/text()").re(r'[\w\s,-\/]*\s48\d{3}\s*\w*')
		informationLink=museum.xpath("div[@id='idContentScroll']/span/a/@href").extract()
		images=sel.xpath("//*[@id='CapaImagen_0']/img/@src").extract()
		museumoReligioso=sel.xpath("//*[@id='see-and-do-content']/section[2]/div/section[1]/section/ul/li/a[@class='sec-bg'][contains(.,'museumos religiosos')]").extract()
		category="Museo"
		category_en="Museum"
		category_eu="Museoa"
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
		if len(images)>0:
			item['image_urls']=[''.join([self.BASE,images.pop()])]
		item['category']=category
		item['category_en']=category_en
		item['category_eu']=category_eu

		enLink=sel.xpath('//*[@id="en"]/@href').extract()
		request=Request(self.BASE+str(enLink.pop()),callback=self.parse_museums_en)
		request.meta['item']=item

		yield request

	def parse_museums_en(self,response):
		sel=Selector(response)
		museum=sel.xpath('//div[@class="col-50 content-desc"]')
		title=museum.xpath("h2[@class='big sec-color']/text()").extract()
		summary=''.join(museum.xpath("div[@id='idContentScroll']/span/p//text()").extract())
		informationLink=museum.xpath("div[@id='idContentScroll']/span/a/@href").extract()
		item = response.meta['item']
		if len(informationLink)>0:
			item['informationLink_en']=informationLink.pop()
		else:
			item['informationLink_en']=response.url
		if len(title)>0:
			item['name_en']=title.pop()
		else:
			item['name_en']=''
		if len(summary)>0:
			item['description_en']=summary
		else:
			item['description_en']=''
		
		euLink=sel.xpath('//*[@id="eu"]/@href').extract()
		request=Request(self.BASE+str(euLink.pop()),callback=self.parse_museums_eu)
		request.meta['item']=item
		yield request

	def parse_museums_eu(self,response):
		sel=Selector(response)
		museum=sel.xpath('//div[@class="col-50 content-desc"]')
		title=museum.xpath("h2[@class='big sec-color']/text()").extract()
		summary=''.join(museum.xpath("div[@id='idContentScroll']/span/p//text()").extract())
		informationLink=museum.xpath("div[@id='idContentScroll']/span/a/@href").extract()
		item = response.meta['item']
		if len(informationLink)>0:
			item['informationLink_eu']=informationLink.pop()
		else:
			item['informationLink_eu']=response.url
		if len(title)>0:
			item['name_eu']=title.pop()
		else:
			item['name_eu']=''
		if len(summary)>0:
			item['description_eu']=summary
		else:
			item['description_eu']=''
		return item
