from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
from demo.items import Item
import datetime
from scrapy.contrib.spiders import XMLFeedSpider
from demo.items import BilbaoItem
import re

class BilbaoRSSSpider(XMLFeedSpider):
	BASE='http://www.bilbao.net'
	name='bilbaorss_spider'
	allowed_domains=['bilbao.net']
	start_urls=["http://www.bilbao.net/cs/Satellite?language=es&pageid=3002273335&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda","http://www.bilbao.net/cs/Satellite?language=es&pageid=3002273835&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda"]
	iterator = 'iternodes' # This is actually unnecessary, since it's the default value
	itertag = 'item'
	def parse_node(self, response, node):
		#item = Item()
		#item['title'] = node.xpath('title').extract()
		links= node.xpath('link/text()').extract()
		#item['description'] = node.xpath('description').extract()
		#print item
		for link in links:
			#print link
			yield Request(link,callback=self.parse_events_links)

	def parse_events_links(self,response):
		sel=Selector(response)
		event=sel.xpath('//div[@id="content"]/div[@class="cont-txt-nivel3"]/div[@id="cont-readspeaker"]')
		title=event.xpath("div[@class='titular']/h3/text()").extract()
		startDate=event.xpath("dl[@class='lista_dl']/dd/text()").re(r"\d{2}[-]\d{2}[-]\d{4}")
		#Como mirar si tiene mas deun horario.
		hour=event.xpath("dl[@class='lista_dl']/dd/text()").re(r"\d{2}[:]\d{2}")
		relativeLink=event.xpath("dl[@class='lista_dl']/dd/a/@href").extract()
		item=BilbaoItem()
		item['title']=title[0].strip()
		print title[0]
		if(len(startDate)>1):
			item['startDate']=startDate[0]
			item['endDate']=startDate[1]
		if(len(hour)==1):
			item['hour']=hour[0]
		else:
			item['hour']='00:00'
		if len(relativeLink)>0:
			url=self.BASE+relativeLink[0]
			request= Request(url, callback=self.getLocationDirection)
			request.meta['item']=item
			return request
		else:
			alternativeLocation=event.xpath("dl[@class='lista_dl']/dd/text()").extract()
			if len(alternativeLocation)>0:
				pattern=re.compile(r"(?P<date>\d{2}-\d{2}-\d{4})|(?P<time>\d{2}:\d{2})")
				location=pattern.sub("",alternativeLocation[len(alternativeLocation)-1])
				if location:
					item['location']=location
					return item

	def getLocationDirection(self, response):
		sel=Selector(response)
		location=sel.xpath("//div[@id='content']/div[@class='cont-txt-nivel3']/div[@id='cont-readspeaker']/dl/dd/text()").re(r'[\w\s]*\s48\d{3}\s*\w*')
		item = response.meta['item']
		item['location']=location[0]
		return item