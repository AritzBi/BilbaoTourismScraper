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
	#Nombre del spider
	name="kedin_spider"
	BASE='http://www.kedin.es'
	#Los dominios permitidos, para evitar ir a webs externas
	allowed_domains=["kedin.es"]
	#Las URLs de inicio del spider, de donde va a empezar el proceso.
	"""start_urls=["http://kedin.es/vizcaya/conciertos-de-pop/feed.rss",
	"http://kedin.es/alava/conciertos-de-pop/feed.rss",
	"http://kedin.es/guipuzcoa/conciertos-de-pop/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-rock/feed.rss",
	"http://kedin.es/alava/conciertos-de-rock/feed.rss",
	"http://kedin.es/guipuzcoa/conciertos-de-rock/feed.rss",
	"http://kedin.es/vizcaya/clasica/feed.rss",
	"http://kedin.es/alava/clasica/feed.rss",
	"http://kedin.es/guipuzcoa/clasica/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-electronica/feed.rss",
	"http://kedin.es/alava/conciertos-de-electronica/feed.rss",
	"http://kedin.es/guipuzcoa/conciertos-de-electronica/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-indie/feed.rss",
	"http://kedin.es/guipuzcoa/conciertos-de-indie/feed.rss",
	"http://kedin.es/alava/conciertos-de-indie/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-musica/feed.rss",
	"http://kedin.es/alava/conciertos-de-musica/feed.rss",
	"http://kedin.es/guipuzcoa/conciertos-de-musica/feed.rss",
	"http://kedin.es/vizcaya/festivales/feed.rss",
	"http://kedin.es/alava/festivales/feed.rss",
	"http://kedin.es/guipuzcoa/festivales/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-heavy/feed.rss",
	"http://kedin.es/alava/conciertos-de-heavy/feed.rss",
	"http://kedin.es/guipuzcoa/conciertos-de-heavy/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-jazz/feed.rss",
	"http://kedin.es/alava/conciertos-de-jazz/feed.rss",
	"http://kedin.es/guipuzcoa/conciertos-de-jazz/feed.rss",
	"http://kedin.es/vizcaya/arte-cultura/feed.rss",
	"http://kedin.es/guipuzcoa/arte-cultura/feed.rss",
	"http://kedin.es/alava/arte-cultura/feed.rss",
	"http://kedin.es/vizcaya/teatro/feed.rss",
	"http://kedin.es/alava/teatro/feed.rss"
	"http://kedin.es/guipuzcoa/teatro/feed.rss"
	"http://kedin.es/vizcaya/musicales/feed.rss",
	"http://kedin.es/guipuzcoa/musicales/feed.rss",
	"http://kedin.es/alava/musicales/feed.rss",
	"http://kedin.es/vizcaya/monologos-humor/feed.rss",
	"http://kedin.es/alava/monologos-humor/feed.rss",
	"http://kedin.es/guipuzcoa/monologos-humor/feed.rss",
	"http://kedin.es/vizcaya/danza-baile/feed.rss",
	"http://kedin.es/alava/danza-baile/feed.rss",
	"http://kedin.es/guipuzcoa/danza-baile/feed.rss",
	"http://kedin.es/vizcaya/actividades-para-ninos/feed.rss",
	"http://kedin.es/alava/actividades-para-ninos/feed.rss",
	"http://kedin.es/guipuzcoa/actividades-para-ninos/feed.rss",
	"http://kedin.es/vizcaya/tendencias/feed.rss",
	"http://kedin.es/alava/tendencias/feed.rss",
	"http://kedin.es/guipuzcoa/tendencias/feed.rss"]"""
	start_urls=["http://kedin.es/vizcaya/conciertos-de-pop/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-rock/feed.rss",
	"http://kedin.es/vizcaya/clasica/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-electronica/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-indie/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-musica/feed.rss",
	"http://kedin.es/vizcaya/festivales/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-heavy/feed.rss",
	"http://kedin.es/vizcaya/conciertos-de-jazz/feed.rss",
	"http://kedin.es/vizcaya/arte-cultura/feed.rss",
	"http://kedin.es/vizcaya/teatro/feed.rss",
	"http://kedin.es/vizcaya/musicales/feed.rss",
	"http://kedin.es/vizcaya/monologos-humor/feed.rss",
	"http://kedin.es/vizcaya/danza-baile/feed.rss",
	"http://kedin.es/vizcaya/actividades-para-ninos/feed.rss",
	"http://kedin.es/vizcaya/tendencias/feed.rss"]
	#Nombre del tag de los elementos del RSS
	itertag = 'item'
	#Variable interna de Scrapy
	iterator = 'iternodes'
	"""Primer método que es llamado al iniciar el spider, una vez por cada nodo del RSS. 
	En la varible response tiene el nodo obtenido"""
	def parse_node(self, response, node):
		#Se obtiene el enlace donde hay más información
		link= node.xpath('link/text()').extract()
		#Se obtiene el titulo del evento
		title= node.xpath('title/text()').extract()
		#Se obtiene la descripción del evento
		description=node.xpath('description/text()').extract()
		#Se crea un item por cada evento
		item=EventItem()
		item['title']=title[0]
		#Se quitan todos los elementos HTML
		description=re.sub('<[^>]*>', '', description[0])
		item['description']=description
		item['informationLink']=link
		#Se crea un objeto request de Scrapy, indicando que enlance tiene que analizar y en qué metodo
		request=Request(link[0],callback=self.parse_events_links)
		#Se añade a la request el Item del evento donde se irá añadiendo la información
		request.meta['item']=item
		#Se hace la request
		yield request



	def parse_events_links(self,response):
		sel=Selector(response)

		startDate=sel.xpath("//*[@id='header']/div[3]/div[1]/header/ul/li[2]/strong/meta[@itemprop='startDate']/@content").extract()
		startDate=startDate.pop()
		endDate=sel.xpath("//*[@id='header']/div[3]/div[1]/header/ul/li[2]/strong[2]/meta[@itemprop='endDate']/@content").extract()
		category=sel.xpath("//*[@id='breadcrumb']/span/a/span/text()").extract()
		moreInformation=sel.xpath("string(//*[@id='description']/div[1]/p)").extract()
		images=sel.xpath("//*[@id='main_content']/article/section[1]/a/img/@src").extract()
		
		if len(endDate)>0:
			endDate=endDate.pop()

			hours=sel.xpath("//*[@id='header']/div[3]/div[1]/header/ul/li[3]/span/strong/text()").re(r"\d{2}[:]\d{2}")	
			if len(hours)==2:
				startHour=hours[0]
				endHour=hours.pop()
		else:
			hours=sel.xpath("//*[@id='header']/div[3]/div[1]/header/ul/li[3]/span/strong/text()").re(r"\d{2}[:]\d{2}")
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
		#priceItemprop=sel.xpath("//*[@id='main_content']/article/section[2]/p[2]/span[1]/span/strong/@itemprop").extract()
		priceItemprop=sel.xpath("//*[@id='header']/div[3]/div[1]/header/ul/li[4]/span/span/strong/@itemprop").extract()
		#print priceItemprop
		#priceClass=sel.xpath("//*[@id='main_content']/article/section[2]/p[2]/span[1]/span/strong/@class").extract()
		priceClass=sel.xpath("//*[@id='header']/div[3]/div[1]/header/ul/li[4]/span/span/strong/@class").extract()
		#print priceClass
		
		#priceArray=sel.xpath("//*[@id='main_content']/article/section[2]/p[2]/span[1]/span/strong/text()").re(r"\d+\,?\d*")
		priceArray=sel.xpath("//*[@id='header']/div[3]/div[1]/header/ul/li[4]/span/span/strong/text()").re(r"\d+\,?\d*")
		#print priceArray
		item['lowPrice']=-1
		item['highPrice']=-1
		rangePrices=False;
		if len(priceClass)>0:
			priceClass=priceClass.pop()
			if priceClass== 'free':
				price=0
				item['lowPrice']=0
				item['highPrice']=0
				rangePrices=False
		elif len(priceItemprop)>0:
			if len(priceItemprop)==2:
				price=priceArray[0]+'-'+priceArray[1]
				priceArray[0]=priceArray[0].replace(',','.')
				priceArray[1]=priceArray[1].replace(',','.')
				item['lowPrice']=float(priceArray[0])
				item['highPrice']=float(priceArray[1])
				rangePrices=True
			else:
				price=priceArray.pop()
				if isinstance(price, str):
					price=pricereplace(',','.')
				item['lowPrice']=float(price)
				item['highPrice']=item['lowPrice']
				rangePrices=False
	
		item['rangePrices']=rangePrices
		#locationURL=sel.xpath("//*[@id='main_content']/article/section[2]/p[2]/span[2]/a/@href").extract()
		locationURL=sel.xpath("//*[@id='header']/div[3]/div[1]/header/ul/li[1]/span/a[1]/@href").extract()
		if len(locationURL)>0:
			request=Request(self.BASE+locationURL[0],callback=self.parse_event_location,dont_filter=True)
			request.meta['item']=item
			yield request
		else:
			#locationName=sel.xpath("//*[@id='main_content']/article/section[2]/p[2]/hspan/span/text()").extract().pop()
			locationName=sel.xpath("//*[@id='header']/div[3]/div[1]/header/ul/li[1]/span/span/text()").extract().pop()
			if "Por confirmar" not in locationName:
				item['locationName']=locationName
				item['lat']=-1
				item['lon']=-1
				item['locationAddress']=locationName
			yield item
	def parse_event_location(self,response):
		item=response.meta['item']
		sel=Selector(response)
		locationName=sel.xpath("//*[@id='header']/div[3]/div[1]/header/h1/text()").extract()
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

