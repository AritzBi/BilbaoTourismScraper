#!/usr/bin/env python
#coding: utf8 
from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
from demo.items import RestaurantItem
import re

class RestaurantesSpider(Spider):
	BASE='http://turismo.euskadi.net'
	name='restaurantes_spider'
	allowed_domains=['turismo.euskadi.net']
	start_urls=['http://turismo.euskadi.net/x65-15634x/es/s12PortalWar/buscadoresJSP/buscadorB1.jsp?r01kLang=es&marks=4&restorationType=R']

	def parse(self,response):
		sel = Selector(response)
		otherURLS = sel.xpath('//*[@id="containerConRutas"]/div[3]/div/div/div/div/div[3]/div/ul')
		relativeURLS=otherURLS.xpath("li[@class='r01NavBarItem r01NavBarIntermediateItem']/a/@href").extract()
		#EL ultimo de la lista tiene una clase diferente.
		lastRelativeURL=otherURLS.xpath("li[@class='r01NavBarItem']/a/@href").extract()
		if len(lastRelativeURL)>0:
			relativeURLS.append(lastRelativeURL.pop())
		moreLinksPage=otherURLS.xpath("li[@class='r01NavBarCtrlItem r01NavBarNextBlock']/a/@href").extract()
		for relativeLink in relativeURLS:
			url=self.BASE+relativeLink
			yield Request(url,callback=self.parse_restaurants_links)
		if len(moreLinksPage)>0:
			url=self.BASE+moreLinksPage.pop()
			yield Request(url)
			yield Request(url,callback=self.parse_restaurants_links,dont_filter=True)
		yield Request(response.url,callback=self.parse_restaurants_links)

	def parse_restaurants_links(self,response):
		sel=Selector(response)
		listings=sel.xpath('//*[@id="containerConRutas"]/div[3]/div/div/div/div/div[2]/ul/li')
		links = []
		for listing in listings:
			link=listing.xpath('div/div/div/a/@href').extract()[0]
			links.append(link)
		for link in links:
			link=self.BASE+link
			yield Request(link,callback=self.parse_events_links)

	def parse_events_links(self,response):
		sel=Selector(response)
		name=sel.xpath("//*[@id='containercontVisual']/div[2]/div[1]/div[1]/h1/span/text()").extract()
		result=sel.xpath("//*[@id='containercontVisual']/div[2]/div[3]/div[2]/div[1]/div")
		category=result.xpath("div[contains(.,'Tipo de ')]/following-sibling::div/text()").extract()
		#Direc por el tema de la tilde, esta vez no lo pilla bien aunque este el encoding bien
		address=result.xpath("div[contains(.,'Direcci')]/following-sibling::div/text()").extract()
		telephone=result.xpath("div[contains(.,'Tel')]/following-sibling::div/text()").extract()
		weeklyRest=result.xpath("div[contains(.,'Descanso')]/following-sibling::div/text()").extract()
		holidays=result.xpath("div[contains(.,'Cierre por')]/following-sibling::div/text()").extract()
		#capacity=result.xpath("div[contains(.,'Capacidad')]/following-sibling::div/text()").extract()
		information=result.xpath("//*[@id='containercontVisual']/div[2]/div[3]/div[2]/div[2]/text()").extract()
		email=result.xpath("div[contains(.,'E-mail')]/following-sibling::div/text()").extract()
		informationLink=response.url
		awards=sel.xpath("//*[@id='containercontVisual']/div[2]/div[2]/div/div/div[2]")
		awards=awards.xpath("div/img/@title").extract()
		repsol=0
		michelin=0
		for award in awards:
			if 'Repsol' in award:
				repsol=re.search(r"\d",award).group()
			elif 'Michelin' in award:
				michelin=re.search(r"\d", award).group()

		if len(name)>0:
			name=name.pop()
				#Mirar el else
			if len(category)>0:	
				item=RestaurantItem()
				item['name']=name
				timetable=''
				if len(weeklyRest)>0:	
					timetable='Descando Semanal: '+weeklyRest.pop()
				if len(holidays)>0:
					timetable=timetable+'. Cierre por vacaciones: '+holidays.pop()
				item['timetable']=timetable
				if len(telephone)>0:	
					item['telephone']=telephone.pop()
				else:
					item['telephone']=''
				if len(email)>0:
					item['email']=email.pop()
				else:
					item['email']=''
				item['repsol']=repsol
				item['michelin']=michelin
				item['informationLink']=informationLink
				if len(address)>0:
					if len(address)>2:
						postalCode=re.search(r"48\d{3}",address[1])
						if postalCode:
							postalCode=postalCode.group()
							item['address']=address[0]+', '+postalCode
					else:
						item['address']=address[0]
				else:
					item['address']=''
				if len(information)>0:
					informationConcatenated=''
					for val in information:
						informationConcatenated=informationConcatenated+val
					item['information']=informationConcatenated
				else:
					item['information']=0
				if len(category)>0:
					item['category']=category.pop()
				else:
					item['category']="Otros"
				print item['category']
