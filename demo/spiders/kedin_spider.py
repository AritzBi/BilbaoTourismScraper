#!/usr/bin/env python
#coding: utf8 
from scrapy.spider import Spider 
from scrapy.selector import Selector
from demo.items import EventItem
from scrapy.http.request import Request
from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.http.request import Request

class KedinSpider(XMLFeedSpider):
	name="kedin_spider"
	allowed_domains=["kedin.es"]
	start_urls=["http://kedin.es/vizcaya/conciertos-de-pop/feed.rss","http://kedin.es/vizcaya/conciertos-de-rock/feed.rss","http://kedin.es/vizcaya/conciertos-de-cantautores.html","http://kedin.es/vizcaya/clasica/feed.rss","http://kedin.es/vizcaya/conciertos-de-electronica/feed.rss","http://kedin.es/vizcaya/conciertos-de-indie.html","http://kedin.es/vizcaya/conciertos-de-musica/feed.rss","http://kedin.es/vizcaya/festivales/feed.rss","http://kedin.es/vizcaya/conciertos-de-heavy/feed.rss","http://kedin.es/vizcaya/conciertos-de-jazz/feed.rss"]
	itertag = 'item'
	iterator = 'iternodes'
	def parse_node(self, response, node):
		links= node.xpath('link/text()').extract()
		titles= node.xpath('title/text()').extract()
		descriptions=node.xpath('description/text()').extract()
		for link,title,description in zip(links,titles,descriptions):
			item=EventItem()
			item['title']=title
			item['description']=description
			item['informationLink']=link
			request=Request(link,callback=self.parse_events_links)
			request.meta['item']=item
			yield request



	def parse_events_links(self,response):
		sel=Selector(response)
		event=sel.xpath("//article/ul[@class='data-info']")
		#print event.extract()
		startDate=event.xpath("li[@class='info']/p[@class='lcontainer']/strong/meta[@itemprop='startDate']/@content").extract()
		endDate=event.xpath("li[@class='info']/p[@class='lcontainer']/strong/meta[@itemprop='endDate']/@content").extract()
		if len(endDate)>0:
			
		else:
			endHour=event.xpath("li[@class='time']/p[@class='lcontainer']/strong/text()").re(r"\d{2}[:]\d{2}")
			if len(endHour)==2:
				startHour=endHour[0]
				endHour=endHour.pop()
				endDate=startDate.pop().replace(startHour,endHour)
				print endDate

