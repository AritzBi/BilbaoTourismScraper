#!/usr/bin/env python
#coding: utf8 
from scrapy.spider import Spider 
from scrapy.selector import Selector
from demo.items import EventItem
from scrapy.http.request import Request

class DemoSpider(Spider):
	name="antzoki_spider"
	allowed_domains=["kafeantzokia.com"]
	start_urls=["http://www.kafeantzokia.com/web/agenda?lang=es"]
	BASE='http://www.kafeantzokia.com'

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath('//tbody/tr')
		items = []
		for site in sites:
			#The type of item is defined.
			item = EventItem()
			item['title'] = site.xpath("td[@headers='el_title']/a/text()").extract()
			#item['title'] = site.xpath("/td[@headers='el_title']/a/text()").extract()
			item['date'] = site.xpath("td[@headers='el_date']/strong/text()").extract()
			item['hour'] = site.xpath("td[@headers='el_date']/text()").extract()
			item['location'] = site.xpath("td[@headers='el_location']/a/text()").extract()
			item['category'] = site.xpath("td[@headers='el_category']/a/text()").extract()
			relativeLink=site.xpath("td[@headers='el_title']/a/@href").extract()
			url=self.BASE+relativeLink[0]
			request= Request(url, callback=self.getPrice)
			request.meta['item']=item
			yield request
			#items.append(item)
		#return items

	def getPrice (self, response):
		sel=Selector(response)
		precioAnticipada=sel.xpath("//body/div/div/div/div/div/div/div/div/p/strong/text()").re(r'Anticipada:\s*\d+\s*')
		precioTaquilla=sel.xpath("//body/div/div/div/div/div/div/div/div/p/strong/text()").re(r'Taquilla:\s*\d+\s*|Entrada:\s*\d+\s*')
		precioGratis=sel.xpath("//body/div/div/div/div/div/div/div/div/p/strong/text()").re(r'Entrada\slibre|Entrada\sgratuita')
		item = response.meta['item']
		item['informationLink']=response.url
		if len(precioAnticipada)!=0:
			#print "Precio Anticipada: "+precioAnticipada[0]
			precioAnticipada=precioAnticipada[0].split(':')
			#print "Precio Anticipada: "+precioAnticipada.pop()
			item['priceAnticipada']=precioAnticipada.pop()
		else:
			item['priceAnticipada']=-1
		if len(precioTaquilla)!=0:
			precioTaquilla=precioTaquilla[0].split(':')
			#print "Precio Taquilla: "+precioTaquilla.pop()
			item['priceTaquilla']=precioTaquilla.pop()
		else:
			item['priceTaquilla']=-1
		if len(precioGratis)!=0:
			#print "Precio Gratis"
			item['priceTaquilla']=0
		return item
		