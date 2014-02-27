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
		barAddress=bar.xpath("p/strong[contains(.,'Lugar:')]/following-sibling::text()[2]").extract()
		barTimetable=bar.xpath("p/strong[contains(.,'Horario:')]/following-sibling::text()[1]").extract()
		barTelephone=bar.xpath("p/strong[contains(.,'Tel')]/following-sibling::text()[1]").extract()
		barLocality=bar.xpath("p/strong[contains(.,'Localidad:')]/following-sibling::text()[1]").extract()
		barProvince=bar.xpath("p/strong[contains(.,'Provincia:')]/following-sibling::text()[1]").extract()
		#barSpecialty=sel.xpath("//*[@id='wn_textolargo']/div/p[3]/strong[contains(.,'Especialidad:')]/following-sibling::text()[1]").extract()
		information=sel.xpath("//*[@id='wn_textolargo']/div/p//text()").extract()
		if len(barName)>0:
			barName=barName.pop()
			#Para evitar bares donde no hay nombre ni direccion, solo pone una ','
			if re.search(r"\w+",barName):
			#TODO: mirar el else		
				if len(barCategory)>0:	
					category=barCategory.pop()
					if re.search(r"Pintxo",category):
						item=RestaurantItem()
						item['name']=barName
						if len(barSpecialty)>0:
							information=''.join(information)
							print information
							item['information']=information
						else:
							item['information']=''
						if len(barTimetable)>0:	
							item['timetable']=barTimetable.pop()
						else:
							item['timetable']=barTimetable
						if len(barTelephone)>0:	
							item['telephone']=barTelephone.pop()
						else:
							item['telephone']=''
						if len (barAddress)>0:
							address=barAddress.pop()
							comma=' '
							if re.search(r"\d+", address):
								comma=', '
							if len(barLocality)>0:
								locality=barLocality.pop()
								locality=locality.replace('-','')
								locality=locality.replace(' ','')
								address=address+comma+locality
							item['address']=address
						else:
							item['barAddress']=''
						item['category']='Bar Pintxos'
						item['informationLink']=response.url
						return item





