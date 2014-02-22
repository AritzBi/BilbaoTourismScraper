#!/usr/bin/env python
#coding: utf8 
from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector

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
		result=sel.select("//*[@id='containercontVisual']/div[2]/div[3]/div[2]/div[1]/div[1]")
		#print result.extract()
		print result.xpath("div[contains(.,'Tipo de cocina')]/following-sibling::div/text()").extract()
