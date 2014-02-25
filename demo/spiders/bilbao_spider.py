from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
#from demo.items import BilbaoItem
import datetime


class BilbaoSpider(Spider):
	BASE='http://www.bilbaoturismo.net'
	name='bilbao_spider'
	allowed_domains=['bilbaoturismo.net']
	start_urls=['http://www.bilbaoturismo.net/BilbaoTurismo/es/grandes-citas']
	def parse(self, response):
		sel = Selector(response)
		listings = sel.xpath('//section/ul[@class="list-menu sec-color"]/li')
		links = []
		for listing in listings:
			link=listing.xpath('a/@href').extract()[0]
			links.append(link)
		for link in links:
			#yield Request(urlparse.urljoin(response.url,link),callback=self.parse_listing_page)
			year=datetime.date.today().strftime("%Y")
			month=datetime.date.today().strftime("%m")
			year= int(year)
			month=int(month)
			for counter in range(4):
				if(month<10):
					url=self.BASE+str(link)+'?mes='+str(year)+'0'+str(month)
				else:
					url=self.BASE+str(link)+'?mes='+str(year)+str(month)
				if month!=12:
					month+=1
				else:
					month=1
					year+=1
				print url
				yield Request(url,callback=self.parse_events_links)

	def parse_events_links(self,response):
		sel = Selector(response)
		listings = sel.xpath('//section[@class="column x-image"]')
		links = []
		for listing in listings:
			link=listing.xpath('a/@href').extract()[0]
			links.append(link)
		for link in links:
			yield Request(self.BASE+str(link),callback=self.parse_events)


	def parse_events(self,response):
		"""sel=Selector(response)
		event=sel.xpath('//div[@class="col-50 content-desc"]')
		item=BilbaoItem()
		item['title']=event.xpath("h2[@class='big sec-color']/text()").extract()
		item['startDate']=event.xpath("span/meta[@itemprop='startDate']/@content").extract()
		item['endDate']=event.xpath("span/meta[@itemprop='endDate']/@content").extract()
		item['summary']=event.xpath("div[@id='idContentScroll']/span/p/text()").extract()
		item['location']=event.xpath("span/strong/span/span[@itemprop='name']/text()").extract()
		item['nearestMetro']=event.xpath("span[@itemprop='address']/text()").extract()
		item['postalCode']=event.xpath("span/span[@itemprop='postalCode']/text()").extract()
		item['city']=event.xpath("span/span[@itemprop='addressLocality']/text()").extract()
		return item"""