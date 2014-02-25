from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
from demo.items import RestaurantItem
import re

class RestaurantesSpider(Spider):
	name='barespintxos_spider'
	allowed_domains=['servicios.elcorreo.com']
	start_urls=['http://servicios.elcorreo.com/gastronomia/guia-bares/vizcaya-bilbao.html']

	def parse(self, response):
		sel=Selector(response)
		#print response.body

		listing=sel.xpath("//*[@id='contenido']/div/div/div/table[@id='colAB']/tr/td/div").extract()
		listing=sel.xpath("//*[@id='colAB']/tr[2]/td/table/tr/td[3]/h2[contains(.,'Pintxos')]/following-sibling::div/a/@href").extract()
		for link in listing:
			yield Request(link,callback=self.parse_bar_links)

	def parse_bar_links(self,response):
		sel=Selector(response)
		bar=sel.xpath("//*[@id='texto']/table/tbody/tr[1]/td/div")
		barCategory=bar.xpath("h3/text()").extract()
		barName=bar.xpath("p/strong[contains(.,'Lugar:')]/following-sibling::text()[1]").extract()
		barAddress=bar.xpath("p/strong[contains(.,'Lugar:')]/following-sibling::br/text()[1]").extract()
		barTimetable=bar.xpath("p/strong[contains(.,'Horario:')]/following-sibling::text()[1]").extract()
		barTelephone=bar.xpath("p/strong[contains(.,'Tel')]/following-sibling::text()[1]").extract()
		barLocality=bar.xpath("p/strong[contains(.,'Localidad:')]/following-sibling::text()[1]").extract()
		barProvince=bar.xpath("p/strong[contains(.,'Provincia:')]/following-sibling::text()[1]").extract()
		barSpecialty=sel.xpath("//*[@id='wn_textolargo']/div/p[3]/strong[contains(.,'Especialidad:')]/following-sibling::text()[1]")
		item=RestaurantItem()
		if len(barSpecialty)>0:
			item['specialty']=barSpecialty.pop()
		else:
			item['specialty']=''
		if len(barName)>0:
			item['name']=barName.pop()
		else:
			item['name']=''
		if len(barCategory)>0:	
			item['category']=barCategory.pop()
		else:
			item['category']=''
		if len(barTimetable)>0:	
			item['timetable']=barTimetable.pop()
		else:
			item['timetable']=barTimetable
		if len(barTelephone)>0:	
			item['telephone']=barTelephone.pop()
		else:
			item['telephone']=''

		print barAddress



