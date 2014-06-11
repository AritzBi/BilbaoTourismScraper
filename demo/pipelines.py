#!/usr/bin/env python
#coding: utf8 
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.

import sys
import psycopg2
import pprint
import datetime
import goslate
from scrapy.contrib.pipeline.images import ImagesPipeline
from geopy import geocoders
from scrapy.http.request import Request

class MyImagesPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		item['image_paths'] ="Item contains no images"
		for image_url in item['image_urls']:
			yield Request(image_url)
	def item_completed(self, results, item, info):
		image_paths = [x['path'] for ok, x in results if ok]
		if not image_paths:
			item['image_paths'] ="Item contains no images"
		else:
			item['image_paths'] = image_paths
		return item

class EventPipeline(object):
	def __init__(self):
		conn_string = "host='localhost' dbname='mydb' user='doctor' password='who'"
		# print the connection string we will use to connect
		print "Connecting to database\n	->%s" % (conn_string)
		# get a connection, if a connect cannot be made an exception will be raised here
		self.conn = psycopg2.connect(conn_string)
		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		self.cursor = self.conn.cursor()
	def process_item(self,item,spider):
		if spider.name == 'bTurismoPatrimonio_spider_es'or spider.name=='museosBTurismo_spider':
			name=item['name']
			name_en=item['name_en']
			name_eu=item['name_eu']
			category=item['category']
			category_en=item['category_en']
			category_eu=item['category_eu']
			address=item['address']
			description=item['description']
			description_eu=item['description_eu']
			description_en=item['description_en']
			informationLink=item['informationLink']
			informationLink_en=item['informationLink_en']
			informationLink_eu=item['informationLink_eu']
			if len(item['image_paths'])>0:
				image_path=item['image_paths'].pop()
			else:
				image_path="Item contains no images"
			#Algunos no tienen bien el addres por eso lo dejo asi
			if address:
				coordinates=self.getCoordinates(address.encode('utf-8'))
				longitude=coordinates[1]
				latitude=coordinates[0]
				self.insertPatrimonioToDB(name,name_en,name_eu,category,category_en,category_eu,address,description, description_en,description_eu,informationLink,informationLink_en,informationLink_eu,longitude,latitude,image_path)
		elif spider.name == 'bTurismoPintxos_spider_es' or spider.name=='bTurismoRestaurantes_spider_es':
			name=item['name']
			address=item['address']
			description=item['description']
			description_en=item['description_en']
			description_eu=item['description_eu']
			telephone=item['telephone']
			email=item['email']
			informationLink=item['informationLink']
			category1=item['category'][1]
			category2=item['category'][0]
			category1_en=item['category_en'][1]
			category2_en=item['category_en'][0]
			category1_eu=item['category_eu'][1]
			category2_eu=item['category_eu'][0]
			source_url=item['originLink']
			if spider.name=='bTurismoRestaurantes_spider_es':
				timetable_es=item['timetable']
				timetable_en=item['timetable_en']
				timetable_eu=item['timetable_eu']
			else:
				timetable_es=''
				timetable_en=''
				timetable_eu=''
			if len(item['image_paths'])>0:
				image_path=item['image_paths'].pop()
			else:
				image_path="Item contains no images"
			if address:
				coordinates=self.getCoordinates(address.encode('utf-8'))
				longitude=coordinates[1]
				latitude=coordinates[0]
				self.insertHosteleriaToDB(name,address,description,telephone,email,informationLink,category1,category2,longitude,latitude, image_path, category1_en,category2_en,category1_eu,category2_eu,description_en,description_eu, source_url, timetable_es, timetable_en, timetable_eu)
		elif spider.name=='kedin_spider':
			title=item['title']
			title_en=self.getTranslation(title, 'en')
			title_eu=self.getTranslation(title, 'eu')
			description=item['description']
			description_en=self.getTranslation(description,'en')
			description_eu=self.getTranslation(description, 'eu')
			informationLink=item['informationLink']
			startDate=item['startDate']
			endDate=item['endDate']
			startHour=item['startHour']
			endHour=item['endHour']
			category=item['category']
			locationName=item['locationName']
			address=item['locationAddress']
			price=item['priceTaquilla']
			rangePrices=item['rangePrices']
			longitude=item['lon']
			latitude=item['lat']
			moreInformation=item['moreInformation']
			moreInformation_en=self.getTranslation(moreInformation, 'en')
			moreInformation_eu=self.getTranslation(moreInformation, 'eu')
			category1_es=category[2]
			category1_en=self.getTranslation(category[2],'en')
			category1_eu=self.getTranslation(category[2], 'eu')
			category2_es=category[3]
			category2_en=self.getTranslation(category[3], 'en')
			category2_eu=self.getTranslation(category[3], 'eu')
			if len(item['image_paths'])>0:
				print item['image_paths']
				image_path=item['image_paths'].pop()
			else:
				image_path="Item contains no images"
			"""print "Title: "+title
			print "Description: "+description
			print informationLink
			print "StartDate: "+startDate
			print "endDate: "+endDate
			print "starthour: "+startHour
			print "endHour"+ endHour
			print category
			print "locationName"+locationName
			print "address"+address
			print "price"+str(price)
			print "rangePrices"+str(rangePrices)
			print "longitude"+longitude
			print "latitude"+latitude"""
			self.insertEventToDB(title,title_en, title_eu, description,description_en, description_eu,startDate,endDate,startHour,endHour,category1_es, category1_en, category1_eu, category2_es, category2_en, category2_eu,informationLink,longitude, latitude,price, rangePrices, locationName, address, moreInformation, moreInformation_en, moreInformation_eu,image_path)

		elif spider.name == 'bilbao_spider':
			denomLocation=item['location']
			denomEvent=item['title']
			#price=item['price']
			startDate=item['startDate'][0]
			startDate=startDate.split('-')
			endDate=item['endDate'][0]
			endDate=endDate.split('-')
			if(len(denomLocation)!=0):
				self.insertDataToDB(denomLocation[0], denomEvent[0],1,startDate,endDate,-1)
		elif spider.name == 'antzoki_spider':
			date=item['date'][0]
			date=date.split('.')
			#tiene length 3 y la hora esta en la ultima posicion
			hour=item['hour'][2]
			#En este caso si la hora pasa de las 24, la fecha seria otra.
			if '-' in hour:
				hour=hour.split('-')
				startHour=hour[0].split('.')
				endHour=hour[1].split('.')
				startDate=datetime.datetime.combine(datetime.date(int(date[0]),int(date[1]),int(date[2])),datetime.time(int(startHour[0]),int(startHour[1])))
				endDate=datetime.datetime.combine(datetime.date(int(date[0]),int(date[1]),int(date[2])),datetime.time(int(endHour[0]),int(endHour[1])))
			elif '.' in hour:
				hour=hour.split('.')
				startDate=datetime.datetime.combine(datetime.date(int(date[0]),int(date[1]),int(date[2])),datetime.time(int(hour[0]),int(hour[1])))
				endDate=startDate
			else:
				startDate=datetime.datetime.combine(datetime.date(int(date[0]),int(date[1]),int(date[2])),datetime.time(0,0))
				endDate=startDate	
			self.insertDataToDB(item['location'][0],item ['title'][0],item['priceAnticipada'],item['priceTaquilla'],startDate,endDate, self.getCategoryId(item['category'][0]), item['informationLink'] )
			#'Category: '+ item ['category'][0]
		elif spider.name=='bilbaorss_spider':
			denomEvent=item['title']
			denomLocation=item['location']
			startDate=item['startDate']
			endDate=item['endDate']
			hour=item['hour']
			startDate=startDate.split('-')
			endDate=endDate.split('-')
			hour=hour.split(':')
			startDate=datetime.datetime.combine(datetime.date(int(startDate[2]),int(startDate[1]),int(startDate[0])),datetime.time(int(hour[0]),int(hour[1])))
			endDate=datetime.datetime.combine(datetime.date(int(endDate[2]),int(endDate[1]),int(endDate[0])),datetime.time(int(hour[0]),int(hour[1])))
			self.insertDataToDB(denomLocation, denomEvent,1,startDate,endDate,-1)

 	def insertPatrimonioToDB(self, name,name_en,name_eu, category,category_en, category_eu, address, description,description_en,description_eu, informationLink,informationLink_en,informationLink_eu, lon, lat,image_path):
		SQLSelect="SELECT id FROM EMBLEMATIC_BUILDING WHERE DENOM_ES=%s;"
 		self.cursor.execute(SQLSelect,(name,))
 		try:
			if self.cursor.rowcount==0:
	 			SQLSelect="SELECT id FROM BUILDING_TYPE WHERE TYPE_DENOM_ES=%s;"
		 		self.cursor.execute(SQLSelect,(category,))
				if self.cursor.rowcount==0:
					SQLocation="INSERT INTO BUILDING_TYPE (type_denom_es, type_denom_en, type_denom_eu) VALUES (%s,%s,%s) returning id;"
					self.cursor.execute(SQLocation, (category,category_en,category_eu))
					category_id=self.cursor.fetchone()[0]
				else:
					category_id=self.cursor.fetchone()[0]
				SQLSelect="SELECT id FROM LOCATION WHERE ADDRESS=%s;"
				self.cursor.execute(SQLSelect,(address,))
				if self.cursor.rowcount==0:
					SQLEvent="INSERT INTO LOCATION (address, geom) VALUES (%s, ST_GeomFromText('POINT(%s %s)', 4326)) returning id;"
					self.cursor.execute(SQLEvent, (address,lon,lat))
					location_id=self.cursor.fetchone()[0]
				else:
					location_id=self.cursor.fetchone()[0]
				SQLEvent="INSERT INTO EMBLEMATIC_BUILDING(denom_es,denom_en,denom_eu,location_id, description_es,description_en,description_eu, information_url,INFORMATION_URL_EN ,INFORMATION_URL_EU, BUILDING_TYPE,IMAGE_PATH) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id;"
				self.cursor.execute(SQLEvent, (name,name_en,name_eu,location_id,description,description_en,description_eu,informationLink,informationLink_en,informationLink_eu,category_id,image_path))
			self.conn.commit()
		except Exception as e:
			self.conn.commit()
			#print name
			#print address
			#print informationLink
			print e;

	def insertHosteleriaToDB(self,name,address,description,telephone,email, informationLink,category1,category2,lon,lat, image_path,category1_en,category2_en,category1_eu,category2_eu,description_en,description_eu,source_url, timetable_es, timetable_en, timetable_eu):
		SQLSelect="SELECT id FROM HOSTELERY WHERE DENOM_ES=%s;"
 		self.cursor.execute(SQLSelect,(name,))
 		try:
			if self.cursor.rowcount==0:
	 			SQLSelect="SELECT id FROM HOSTELERY_TYPE WHERE FIRST_TYPE_ES=%s and SECOND_TYPE_ES=%s;"
		 		self.cursor.execute(SQLSelect,(category1,category2))
				if self.cursor.rowcount==0:
					SQLocation="INSERT INTO HOSTELERY_TYPE (FIRST_TYPE_ES, SECOND_TYPE_ES,FIRST_TYPE_EN, SECOND_TYPE_EN,FIRST_TYPE_EU, SECOND_TYPE_EU) VALUES (%s,%s,%s,%s,%s,%s) returning id;"
					self.cursor.execute(SQLocation, (category1,category2,category1_en,category2_en,category1_eu,category2_eu))
					category_id=self.cursor.fetchone()[0]
				else:
					category_id=self.cursor.fetchone()[0]
				SQLSelect="SELECT id FROM LOCATION WHERE ADDRESS=%s;"
				self.cursor.execute(SQLSelect,(address,))
				if self.cursor.rowcount==0:
					SQLEvent="INSERT INTO LOCATION (address, geom) VALUES (%s, ST_GeomFromText('POINT(%s %s)', 4326)) returning id;"
					self.cursor.execute(SQLEvent, (address,lon,lat))
					location_id=self.cursor.fetchone()[0]
				else:
					location_id=self.cursor.fetchone()[0]
				SQLEvent="INSERT INTO HOSTELERY(denom_es,location_id, description_es,description_en,description_eu, information_url, HOSTELERY_TYPE, telephone, email, IMAGE_PATH, SOURCE_URL, TIMETABLE_ES, TIMETABLE_EN, TIMETABLE_EU) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s) returning id;"
				self.cursor.execute(SQLEvent, (name,location_id,description,description_en, description_eu,informationLink,category_id,telephone,email,image_path,source_url, timetable_es, timetable_en, timetable_eu ))
			self.conn.commit()
		except Exception as e:
			self.conn.commit()
			print name
			print address
			print informationLink
			print e;

	def insertEventToDB(self, title_es,title_en, title_eu, description_es, description_en, description_eu, startDate, endDate, startHour, endHour, category1_es,category1_en,category1_eu, category2_es,category2_en,category2_eu, informationLink, longitude, latitude, price, rangePrices, locationName, address,moreInformation_es, moreInformation_en, moreInformation_eu,image_path):
 		try:
 			SQL="SELECT s.id FROM EVENT_TYPE t, EVENT_SUBTYPE s WHERE t.TYPE_ES=%s and s.SUBTYPE_ES=%s and s.type_id=t.id;"
 			self.cursor.execute(SQL,(category1_es,category2_es))
			if self.cursor.rowcount==0:
				SQL="SELECT id FROM EVENT_TYPE WHERE TYPE_ES=%s;"
				self.cursor.execute(SQL,(category1_es,))
				if self.cursor.rowcount==0:
					SQL="INSERT INTO EVENT_TYPE(TYPE_ES, TYPE_EN, TYPE_EU) VALUES (%s,%s,%s) returning id;"
					self.cursor.execute(SQL,(category1_es,category1_en, category1_eu))
					category1_id=self.cursor.fetchone()[0]
					SQL="INSERT INTO EVENT_SUBTYPE(SUBTYPE_ES,SUBTYPE_EN, SUBTYPE_EU, type_id) VALUES (%s,%s,%s, %s) returning id;"
					self.cursor.execute(SQL,(category2_es,category2_en, category2_eu,category1_id))
					category_id=self.cursor.fetchone()[0]
				else:
					category1_id=self.cursor.fetchone()[0]
					SQL="INSERT INTO EVENT_SUBTYPE(SUBTYPE_ES,SUBTYPE_EN, SUBTYPE_EU, type_id) VALUES (%s,%s,%s, %s) returning id;"
					self.cursor.execute(SQL,(category2_es,category2_en, category2_eu,category1_id))
					category_id=self.cursor.fetchone()[0]
			else:
				category_id=self.cursor.fetchone()[0]
			SQL="SELECT id FROM LOCATION WHERE ADDRESS=%s;"
			self.cursor.execute(SQL,(address,))
			if self.cursor.rowcount==0:
				SQL="INSERT INTO LOCATION ( address, geom) VALUES ( %s, ST_GeomFromText('POINT(%s %s)', 4326)) returning id;"
				self.cursor.execute(SQL, (address,float(longitude),float(latitude)))
				location_id=self.cursor.fetchone()[0]
			else:
				location_id=self.cursor.fetchone()[0]
			SQL="INSERT INTO EVENT(title_es,title_en, title_eu, description_es, description_en, description_eu, information_url, startdate,endate, starthour,endhour,type_id, price, range_prices, more_information_es,more_information_en,more_information_eu,image_path ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s) returning id;"
			self.cursor.execute(SQL, (title_es, title_en,title_eu, description_es, description_en, description_eu, informationLink, startDate, endDate, startHour, endHour, category_id, price, rangePrices, moreInformation_es, moreInformation_en, moreInformation_eu,image_path))
			event_id=self.cursor.fetchone()[0]
			SQL="INSERT INTO EVENT_LOCATION(location_id, denom, event_id) VALUES (%s, %s, %s);"
			self.cursor.execute(SQL, (location_id, locationName, event_id))
			self.conn.commit()
		except Exception as e:
			self.conn.commit()
			print e;
 	def getCoordinates(self, denomLocation):
 		try:
 			g=geocoders.GoogleV3()
			place, (lat, lng) = g.geocode(denomLocation)
			return(lat,lng)
		except:
			try:
				g=geocoders.GeoNames(None,'aritzbi',None)
				place, (lat, lng) = g.geocode(denomLocation)
				return(lat,lng)
			except:
				try:		
					g=geocoders.Bing('Ag1Y_zbKfJ-sIea_MXaCdtIgnnYojrBytkIc3Pa0L0JLeKcFBwitYBfJvyak5fhq',timeout=5)
					place, (lat, lng) = g.geocode(denomLocation, True, None, None)
					return(lat,lng)
				except:
					return (0,0)
	def getTranslation(self, sourceText, destLanguage):
		gs=goslate.Goslate()
		return gs.translate(sourceText, destLanguage)

	def getCategoryId(self, denomCategory):
		denomCategory=denomCategory.strip()
		print denomCategory
		if denomCategory=='Club' or denomCategory.encode('utf-8')=='Música':
			SQL="SELECT ID FROM EVENT_TYPE WHERE DENOM='Música';"
			self.cursor.execute(SQL)
			if self.cursor.rowcount!=0:
				#categoryId=self.cursor.fetchone()[0]
				#print 'denomCategory: '+denomCategory +' categoryId: '+str(categoryId)
				return self.cursor.fetchone()[0]
		elif denomCategory=='Danza':
			SQL="SELECT ID FROM EVENT_TYPE WHERE DENOM='Teatro y Danza';"
			self.cursor.execute(SQL)
			if self.cursor.rowcount!=0:
				#categoryId=self.cursor.fetchone()[0]
				#print 'denomCategory: '+denomCategory +' categoryId: '+str(categoryId)
				return self.cursor.fetchone()[0]
		elif denomCategory=='Conferencia' or denomCategory.encode('utf-8')=='Presentación':
			SQL="SELECT ID FROM EVENT_TYPE WHERE DENOM='Jornadas, conferencias y congresos';"
			self.cursor.execute(SQL)
			if self.cursor.rowcount!=0:
				#categoryId=self.cursor.fetchone()[0]
				#print 'denomCategory: '+denomCategory +' categoryId: '+str(categoryId)
				return self.cursor.fetchone()[0]
		elif denomCategory=='Fiesta':
			SQL="SELECT ID FROM EVENT_TYPE WHERE DENOM='Folclore y fiestas populares';"
			self.cursor.execute(SQL)
			if self.cursor.rowcount!=0:
				#categoryId=self.cursor.fetchone()[0]
				#print 'denomCategory: '+denomCategory +' categoryId: '+str(categoryId)
				return self.cursor.fetchone()[0]	
		elif denomCategory.encode('utf-8')=='Proyección':
			SQL="SELECT ID FROM EVENT_TYPE WHERE DENOM='Cine';"
			self.cursor.execute(SQL)
			if self.cursor.rowcount!=0:
				#categoryId=self.cursor.fetchone()[0]
				#print 'denomCategory: '+denomCategory +' categoryId: '+str(categoryId)
				return self.cursor.fetchone()[0]	
		elif denomCategory=='Otros':
			SQL="SELECT ID FROM EVENT_TYPE WHERE DENOM='Otros';"
			self.cursor.execute(SQL)
			if self.cursor.rowcount!=0:
				#categoryId=self.cursor.fetchone()[0]
				#print 'denomCategory: '+denomCategory +' categoryId: '+str(categoryId)
				return self.cursor.fetchone()[0]	
		return -1		



