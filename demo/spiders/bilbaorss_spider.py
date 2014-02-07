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
		print 'llego aqui'
		item = Item()
		item['title'] = node.xpath('title').extract()
		item['link'] = node.xpath('link').extract()
		item['description'] = node.xpath('description').extract()
		print item