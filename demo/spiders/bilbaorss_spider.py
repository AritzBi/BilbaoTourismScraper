#!/usr/bin/env python
#coding: utf8 
from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
from demo.items import Item
import datetime
from scrapy.contrib.spiders import XMLFeedSpider
from demo.items import EventItem
import re

class BilbaoRSSSpider(XMLFeedSpider):
	BASE='http://www.bilbao.net'
	name='bilbaorss_spider'
	allowed_domains=['bilbao.net']
	start_urls=["http://www.bilbao.net/cs/Satellite?language=es&pageid=3002271745&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda","http://www.bilbao.net/cs/Satellite?language=es&pageid=3002273237&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda","http://www.bilbao.net/cs/Satellite?language=es&pageid=3002273326&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda","http://www.bilbao.net/cs/Satellite?language=es&pageid=3002273335&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda","http://www.bilbao.net/cs/Satellite?language=es&pageid=3002273835&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda","http://www.bilbao.net/cs/Satellite?language=es&pageid=3008987718&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda","http://www.bilbao.net/cs/Satellite?language=es&pageid=3002274516&pagename=Bilbaonet%2FPage%2FBIO_suscripcionRSS&tipoSus=Agenda"]
	#start_urls=[""]
	iterator = 'iternodes' # This is actually unnecessary, since it's the default value
	itertag = 'item'
	def parse_node(self, response, node):
		links= node.xpath('link/text()').extract()
		for link in links:
			yield Request(link,callback=self.parse_events_links)

	def parse_events_links(self,response):
		sel=Selector(response)
		event=sel.xpath('//div[@id="content"]/div[@class="cont-txt-nivel3"]/div[@id="cont-readspeaker"]')
		title=event.xpath("div[@class='titular']/h3/text()").extract()
		startDate=event.xpath("dl[@class='lista_dl']/dd/text()").re(r"\d{2}[-]\d{2}[-]\d{4}")
		#Las horas, puede tener ninguna o la de inicio.
		hour=event.xpath("dl[@class='lista_dl']/dd/text()").re(r"\d{2}[:]\d{2}")
		#En este caso los links que están en el apartado de Mas Informacion estan dentro de una <p> Puede haber 0,1,2...Si hay mas de uno <br>TOCHECK
		informationLink=event.xpath("dl[@class='lista_dl']/dd/p/@href").extract()
		observations=event.xpath("dl[@class='lista_dl']/dd/p/text()").extract()
		relativeLink=event.xpath("dl[@class='lista_dl']/dd/a/@href").extract()
		category=sel.xpath('//div[@id="content"]/div[@class="cont-txt-nivel3"]/h2/text()').extract()
		item=EventItem()
		#Remove all the unnecessary blank spaces.
		item['title']=title[0].strip()
		if len(observations) >0:
			item['observations']=observations.pop()
		else:
			item['observations']=''
		#For example: Exposiones - Pintura y escultura
		if(len(category)>0):
			item['category']=category.pop().strip()
		else:
			item['category']=''
		#Check if it has two dates: the initial and the ending one.
		if(len(startDate)>1):
			item['startDate']=startDate[0]
			item['endDate']=startDate[1]
		if(len(hour)==0):
			item['startHour']='10:00'
			item['endHour']='-1'
		#Check if it has an initial time
		if(len(hour)==1):
			item['startHour']=hour.pop()
			item['endHour']='-1'
		#Some cases 18:00/17:30 or even 20:00; dia 23 10:00. 
		elif(len(hour)>=2):	
			#Un Array de 3 posiciones, startDate,endDate, y lo de la hora 
			originalHourFormat=event.xpath("dl[@class='lista_dl']/dd/text()").extract()
			originalHourFormat=originalHourFormat.pop()
			if '/' in originalHourFormat:
				item['startHour']=hour[0]
				item['endHour']=hour[1]
			elif ';' in originalHourFormat:
				item['startHour']=hour[0]
				item['observations']=originalHourFormat
		#Otherwise-->Default
		else:
			item['startHour']='10:00'
		if len(relativeLink)>0:
			url=self.BASE+relativeLink[0]
			request= Request(url, callback=self.getLocationDirection,dont_filter=True)
			request.meta['item']=item
			yield request
		else:
			alternativeLocation=event.xpath("dl[@class='lista_dl']/dd/text()").extract()
			if len(alternativeLocation)>0:
				pattern=re.compile(r"(?P<date>\d{2}-\d{2}-\d{4})|(?P<time>\d{2}:\d{2})")
				location=pattern.sub("",alternativeLocation[len(alternativeLocation)-1])
				if location:
					item['locationName']=location
					print item

	def getLocationDirection(self, response):
		sel=Selector(response)
		locationAdress=sel.xpath("//div[@id='content']/div[@class='cont-txt-nivel3']/div[@id='cont-readspeaker']/dl/dd/text()").re(r'[\w\s]*\s48\d{3}\s*\w*')
		locationName=location=sel.xpath("//div[@id='content']/div[@class='cont-txt-nivel3']/h2/text()").extract()
		locationTelephone=sel.xpath("//div[@id='content']/div[@class='cont-txt-nivel3']/div[@id='cont-readspeaker']/dl/dd/text()").re(r'\d{2}\.\d{3}\.\d{2}\.\d{2}')
		locationWebsite=sel.xpath("//div[@id='content']/div[@class='cont-txt-nivel3']/div[@id='cont-readspeaker']/dl/dd/a[@target='_blank']/@href").extract()
		locationEmail=sel.xpath("//div[@id='content']/div[@class='cont-txt-nivel3']/div[@id='cont-readspeaker']/dl/dd/a/@href").re(r'mailto:([a-zA-Z0-9._@]*)')
		item = response.meta['item']
		if(len(locationAdress)>0):
			item['locationAdress']=locationAdress.pop()
		else:
			item['locationAdress']=''
		if(len(locationName)>0):
			item['locationName']=locationName.pop()
		else:
			item['locationName']=locationName.pop()
		if(len(locationTelephone)>0):
			item['locationTelephone']=locationTelephone.pop().replace(".","")
		else:
			item['locationTelephone']=-1
		if(len(locationWebsite)>0):
			item['locationWebsite']=locationWebsite.pop()
		else:
			item['locationWebsite']=''
		if(len(locationEmail)>0):
			item['locationEmail']=locationEmail.pop()
		else:
			item['locationEmail']=''
		print item