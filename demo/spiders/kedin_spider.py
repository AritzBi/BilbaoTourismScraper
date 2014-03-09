#!/usr/bin/env python
#coding: utf8 
from scrapy.spider import Spider 
from scrapy.selector import Selector
from demo.items import EventItem
from scrapy.http.request import Request
from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.http.request import Request
import re

class KedinSpider(XMLFeedSpider):
	name="kedin_spider"
	BASE='http://www.kedin.es'
	allowed_domains=["kedin.es"]
	start_urls=["http://kedin.es/vizcaya/conciertos-de-pop/feed.rss","http://kedin.es/vizcaya/conciertos-de-rock/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-cantautores.html","http://kedin.es/vizcaya/clasica/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-electronica/feed.rss","http://kedin.es/vizcaya/conciertos-de-indie.html",
	"http://kedin.es/vizcaya/conciertos-de-musica/feed.rss","http://kedin.es/vizcaya/festivales/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-heavy/feed.rss","http://kedin.es/vizcaya/conciertos-de-jazz/feed.rss",
	"http://kedin.es/vizcaya/arte-cultura/feed.rss","http://kedin.es/vizcaya/teatro/feed.rss",
	"http://kedin.es/vizcaya/musicales/feed.rss",
	"http://kedin.es/vizcaya/monologos-humor/feed.rss",
	"http://kedin.es/vizcaya/danza-baile/feed.rss",
	"http://kedin.es/vizcaya/actividades-para-ninos.html",
	"http://kedin.es/vizcaya/tendencias/feed.rss"]
	itertag = 'item'
	iterator = 'iternodes'
	def parse_node(self, response, node):
		links= node.xpath('link/text()').extract()
		titles= node.xpath('title/text()').extract()
		descriptions=node.xpath('description/text()').extract()
		for link,title,description in zip(links,titles,descriptions):
			item=EventItem()
			item['title']=title
			description=re.sub('<[^>]*>', '', description)
			item['description']=description
			item['informationLink']=link
			request=Request(link,callback=self.parse_events_links)
			request.meta['item']=item
			yield request



	def parse_events_links(self,response):
		sel=Selector(response)
		event=sel.xpath("//article/ul[@class='data-info']")
		startDate=event.xpath("li[@class='info']/p[@class='lcontainer']/strong/meta[@itemprop='startDate']/@content").extract()
		startDate=startDate.pop()
		endDate=event.xpath("li[@class='info']/p[@class='lcontainer']/strong/meta[@itemprop='endDate']/@content").extract()
		category=sel.xpath("//header/div['@id=breadcrumb']/span/a/span/text()").extract()
		if len(endDate)>0:
			endDate=endDate.pop()
			hours=event.xpath("li[@class='time']/p[@class='lcontainer']/strong/text()").re(r"\d{2}[:]\d{2}")
			if len(hours)==2:
				startHour=hours[0]
				endHour=hours.pop()
		else:
			hours=event.xpath("li[@class='time']/p[@class='lcontainer']/strong/text()").re(r"\d{2}[:]\d{2}")
			if len(hours)==2:
				startHour=hours[0]
				endHour=hours.pop()
				endDate=startDate.replace(startHour,endHour)
		item = response.meta['item']
		item['startDate']=startDate
		item['endDate']=endDate
		item['startHour']=startHour
		item['endHour']=endHour
		item['category']=category
		priceItemprop=event.xpath("li[@class='price']/p[@class='lcontainer']/span/strong/@itemprop").extract()
		priceClass=event.xpath("li[@class='price']/p[@class='lcontainer']/span/strong/@class").extract()
		price=event.xpath("li[@class='price']/p[@class='lcontainer']/span/strong/text()").re(r"\d+")
		rangePrices=False;
		if len(priceClass)>0:
			priceClass=priceClass.pop()
			if priceClass== 'free':
				price=0
			elif priceClass=='undefined':
				price=-1

		elif len(priceItemprop)>0:
			if len(priceItemprop)==2:
				price=price[0]+'-'+price[1]
				rangePrices=True
			else:
				priceItemprop=priceItemprop.pop()
				if(priceItemprop == 'price'):
					price=price.pop()
				elif priceItemprop=='highPrice':
					price=price.pop()
					rangePrices=True;
		item['priceTaquilla']=price
		item['rangePrices']=rangePrices
		locationURL=event.xpath("li[@class='place'][@itemprop='location']/p[@class='lcontainer']/a/@href").extract()
		if len(locationURL)>0:
			request=Request(self.BASE+locationURL[0],callback=self.parse_event_location)
			request.meta['item']=item
			yield request

	def parse_event_location(self,response):
		item=response.meta['item']
		sel=Selector(response)
		location=sel.xpath("//body/div/div/article/div/div/section[@id='place']")
		locationName=location.xpath("p/strong/text()").extract()
		locationAdress=location.xpath("p[@class='address']/text()").extract()
		lat=location.xpath("div[@id='map']/@data-lat").extract()
		lon=location.xpath("div[@id='map']/@data-lng").extract()
		if len(locationName)>0:
			item['locationName']=locationName.pop()
		else:
			item['locationName']=''
		if len(locationAdress)>0:
			item['locationAdress']=locationAdress.pop()
		else:
			item['locationAdress']=''
		if len(lat)>0:
			item['lat']=lat.pop()
		else:
			item['lat']=-1
		if len(lon)>0:
			item['lon']=lon.pop()
		else:
			item['lon']=-1
		
		print item

