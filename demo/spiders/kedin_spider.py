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
	start_urls=["http://kedin.es/vizcaya/conciertos-de-pop/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-rock/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-cantautores.html",
	"http://kedin.es/vizcaya/clasica/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-electronica/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-indie.html",
	"http://kedin.es/vizcaya/conciertos-de-musica/feed.rss",
	"http://kedin.es/vizcaya/festivales/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-heavy/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-jazz/feed.rss",
	"http://kedin.es/vizcaya/arte-cultura/feed.rss",
	"http://kedin.es/vizcaya/teatro/feed.rss",
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
		startDate=sel.xpath("//*[@id='main_content']/article/section[1]/div/strong/meta[@itemprop='startDate']/@content").extract()
		startDate=startDate.pop()
		endDate=sel.xpath("//*[@id='main_content']/article/section[1]/div/strong[2]/meta[@itemprop='endDate']/@content").extract()
		category=sel.xpath("//*[@id='breadcrumb']/span/a/span/text()").extract()
		moreInformation=sel.xpath("string(//*[@id='description']/div[1]/p)").extract()
		images=sel.xpath("//*[@id='main_content']/article/section[2]/a/img/@src").extract()
		if len(endDate)>0:
			endDate=endDate.pop()
			hours=sel.xpath("//*[@id='main_content']/article/section[1]/p[2]/span/strong/text()").re(r"\d{2}[:]\d{2}")	
			if len(hours)==2:
				startHour=hours[0]
				endHour=hours.pop()
		else:
			hours=sel.xpath("//*[@id='main_content']/article/section[1]/p[2]/span/strong/text()").re(r"\d{2}[:]\d{2}")
			if len(hours)==2:
				startHour=hours[0]
				endHour=hours.pop()
				endDate=startDate.replace(startHour,endHour)
			else: 
				startHour=hours[0]


		item = response.meta['item']
		item['startDate']=startDate
		item['endDate']=endDate
		item['startHour']=startHour
		item['endHour']=endHour
		item['category']=category
		if len(moreInformation)>0:
			item['moreInformation']=moreInformation.pop()
		else:
			item['moreInformation']=''
		if len(images)>0:
			#item['image_urls']=[''.join([self.BASE,images.pop()])]
			item['image_urls']=images
		priceItemprop=sel.xpath("//*[@id='main_content']/article/section[1]/p[2]/span[1]/span/strong/@itemprop").extract()
		priceClass=sel.xpath("//*[@id='main_content']/article/section[1]/p[2]/span[1]/span/strong/@class").extract()
		priceArray=sel.xpath("//*[@id='main_content']/article/section[1]/p[2]/span[1]/span/strong/text()").re(r"\d+\,?\d*")
		price=-1
		rangePrices=False;
		if len(priceClass)>0:
			priceClass=priceClass.pop()
			if priceClass== 'free':
				price=0
				rangePrices=False
		elif len(priceItemprop)>0:
			if len(priceItemprop)==2:
				price=priceArray[0]+'-'+priceArray[1]
				rangePrices=True
			else:
				priceItemprop=priceItemprop.pop()
				if(priceItemprop == 'lowPrice'):
					price=priceArray.pop()
					rangePrices=False
				elif priceItemprop=='highPrice':
					price=priceArray.pop()
					rangePrices=False
		
		item['priceTaquilla']=price
		item['rangePrices']=rangePrices
		print price
		print rangePrices
		locationURL=sel.xpath("//*[@id='main_content']/article/section[1]/p[2]/span[2]/a/@href").extract()
		if len(locationURL)>0:
			request=Request(self.BASE+locationURL[0],callback=self.parse_event_location,dont_filter=True)
			request.meta['item']=item
			yield request
		else:
			locationName=sel.xpath("//*[@id='main_content']/article/section[1]/p[2]/hspan/span/text()").extract().pop()
			if "Por confirmar" not in locationName:
				item['locationName']=locationName
				item['lat']=-1
				item['lon']=-1
				item['locationAddress']=locationName
	def parse_event_location(self,response):
		item=response.meta['item']
		sel=Selector(response)
		locationName=sel.xpath("//*[@id='header']/div[2]/div[1]/header/h1/text()").extract()
		locationAdress=sel.xpath("//*[@id='place']/p[2]/text()").extract()
		lon=sel.xpath("//*[@id='map']/@data-lng").extract()
		lat=sel.xpath("//*[@id='map']/@data-lat").extract()
		if len(locationName)>0:
			item['locationName']=locationName.pop()
		else:
			item['locationName']=''
		if len(locationAdress)>0:
			item['locationAddress']=locationAdress.pop()
		else:
			item['locationAddress']=''
		if len(lat)>0:
			item['lat']=lat.pop()
		else:
			item['lat']=-1
		if len(lon)>0:
			item['lon']=lon.pop()
		else:
			item['lon']=-1
		return item

