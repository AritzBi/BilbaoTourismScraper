from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
from demo.items import RestaurantItem
import datetime

#Restaurantes
#TODO: Si no hay URL poner response.url
#Posible: Metro cercano
class RestaurantesBilbaoTurismoSpider(Spider):
	BASE='http://www.bilbaoturismo.net'
	name='bTurismoRestaurantes_spider_es'
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
		description=descriptionpath.xpath("span[@itemprop='description']/p[1]//text()").extract()
		timetable=descriptionpath.xpath("span[@itemprop='description']/p[2]//text()").extract()
		timetable2=descriptionpath.xpath("span[@itemprop='description']/p[3]//text()").extract()
		informationLink=descriptionpath.xpath("span/a/@href").extract()
		categoryPath=sel.xpath("//*[@id='gastronomy-content']/section[2]/div/section[1]/section/div/ul/li[2]/p[2]")
		category=categoryPath.xpath("a/strong/text()").extract()
		images=sel.xpath("//*[@id='CapaImagen_0']/img/@src").extract();
		item=RestaurantItem()
		if len(name)>0:
			item['name']=name.pop()
		else:
			item['name']=''
		if len(streetAddress)>0:
			fullAddress=streetAddress.pop()
			if len(postalCode)>0:
				fullAddress=', '.join([fullAddress,postalCode.pop()])
			if len(addressLocality)>0:
				fullAddress=', '.join([fullAddress,addressLocality.pop()])
			item['address']=fullAddress
		else:
			item['address']=''
		if len(telephone)>0:
			item['telephone']=telephone.pop()
		else:
			item['telephone']=''
		if len(email)>0:
			item['email']=email.pop()
		else:
			item['email']=''
		if len(description)>0:
			item['description']=' '.join(description)
		else:
			item['description']=''
		if len(timetable)>0:
			if len(timetable2)>0:
				item['timetable']=' '.join([timetable.pop(),timetable2.pop()])
			else:
				item['timetable']=timetable.pop()
		else:
			item['timetable']=''
		if len(informationLink)>0:
			item['informationLink']=informationLink.pop()
		else:
			item['informationLink']=''		
		if len(category)>0:
			item['category']=['Restaurante',category.pop()]	
		else:
			item['category']=['Restaurante','Otros']
		if len(images)>0:
			item['image_urls']=[''.join([self.BASE,images.pop()])]
		item['originLink']=response.url
		link=response.url
		print link
		link=link.replace("/es/","/en/")
		request=Request(link,callback=self.parse_restaurants_en)
		request.meta['item']=item
		print item['timetable']

		yield request

	def parse_restaurants_en(self,response):
		sel=Selector(response)
		item = response.meta['item']
		descriptionpath=sel.xpath("//*[@id='idContentScroll']")
		description=descriptionpath.xpath("span[@itemprop='description']/p//text()").extract()
		timetable=descriptionpath.xpath("span[@itemprop='description']/p[2]//text()").extract()
		timetable2=descriptionpath.xpath("span[@itemprop='description']/p[3]//text()").extract()
		categoryPath=sel.xpath("//*[@id='gastronomy-content']/section[2]/div/section[1]/section/div/ul/li[2]/p[2]")
		category=categoryPath.xpath("a/strong/text()").extract()
		if len(description)>0:
			item['description_en']=' '.join(description)
		else:
			item['description_en']=''
		if len(category)>0:
			item['category_en']=['Restaurant',category.pop()]	
		else:
			item['category_en']=['Restaurant','Others']
		if len(timetable)>0:
			if len(timetable2)>0:
				item['timetable_en']=' '.join([timetable.pop(),timetable2.pop()])
			else:
				item['timetable_en']=timetable.pop()
		else:
			item['timetable_en']=''
		link=response.url
		link=link.replace("/en/","/eu/")
		request=Request(link,callback=self.parse_restaurants_eu)
		request.meta['item']=item
		yield request		
		
	def parse_restaurants_eu(self,response):		
		sel=Selector(response)
		item = response.meta['item']
		descriptionpath=sel.xpath("//*[@id='idContentScroll']")
		timetable=descriptionpath.xpath("span[@itemprop='description']/p[2]//text()").extract()
		timetable2=descriptionpath.xpath("span[@itemprop='description']/p[3]//text()").extract()
		description=descriptionpath.xpath("span[@itemprop='description']/p//text()").extract()
		categoryPath=sel.xpath("//*[@id='gastronomy-content']/section[2]/div/section[1]/section/div/ul/li[2]/p[2]")
		category=categoryPath.xpath("a/strong/text()").extract()
		if len(description)>0:
			item['description_eu']=' '.join(description)
		else:
			item['description_eu']=''
		if len(category)>0:
			item['category_eu']=['Jatexea',category.pop()]	
		else:
			item['category_eu']=['Jatexea','Besteak']
		if len(timetable)>0:
			if len(timetable2)>0:
				item['timetable_eu']=' '.join([timetable.pop(),timetable2.pop()])
			else:
				item['timetable_eu']=timetable.pop()
		else:
			item['timetable_eu']=''
		return item