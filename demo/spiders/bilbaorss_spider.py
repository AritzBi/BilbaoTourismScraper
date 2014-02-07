from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
from demo.items import Item
import datetime
from scrapy.contrib.spiders import XMLFeedSpider

class BilbaoRSSSpider(XMLFeedSpider):
	name='bilbaorss_spider'
	allowed_domains=['bilbao.net']
	start_urls=["http://www.bilbao.net/cs/Satellite?language=es&pageid=3002273335&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda"]
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
		print 'ha llegado'
		sel=Selector(response)
		event=sel.xpath('//div[@id="content"]/div[@class="cont-txt-nivel3"]/div[@id="cont-readspeaker"]')
		title=event.xpath("div[@class='titular']/h3/text()").extract()
		startDate=event.xpath("dl[@class='lista_dl']/dd/text()").extract()
		print title
		print startDate
		#item['endDate']=event.xpath("span/meta[@itemprop='endDate']/@content").extract()
		#item['']=event.xpath("div[@id='idContentScroll']/span/p/text()").extract()
		#item['']=event.xpath("span/strong/span/span[@itemprop='name']/text()").extract()
