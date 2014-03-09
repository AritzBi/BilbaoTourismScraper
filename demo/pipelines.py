#!/usr/bin/env python
#coding: utf8 
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.

import sys
import psycopg2
from pygeocoder import Geocoder
import pprint
import datetime
from geopy import geocoders


class DemoPipeline(object):
    def process_item(self, item, spider):
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
		if spider.name == 'bTurismoPatrimonio_spider_es':
			name=item['name']
			category=item['category']
			address=item['address']
			description=item['description']
			informationLink=item['informationLink']
			#Algunos no tienen bien el addres por eso lo dejo asi
			if address:
				coordinates=self.getCoordinates(address.encode('utf-8'))
				longitude=coordinates[0]
				latitude=coordinates[1]
				self.insertPatrimonioToDB(name,category,address,description,informationLink,longitude,latitude)
		elif spider.name == 'bTurismoPintxos_spider_es' or spider.name=='bTurismoRestaurantes_spider_es':
			name=item['name']
			address=item['address']
			description=item['description']
			telephone=item['telephone']
			email=item['email']
			informationLink=item['informationLink']
			category1=item['category'][0]
			category2=item['category'][1]
			if address:
				coordinates=self.getCoordinates(address.encode('utf-8'))
				longitude=coordinates[0]
				latitude=coordinates[1]
		elif spider.name=='kedin_spider':
			title=item['title']
			description=item['description']
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

	def insertDataToDB(self, denomLocation, denomEvent, price_anticipada,price, startDate, endDate, categoryId, information_url):
		denomLocation=denomLocation.split('y')
		listLocations=[]
		listLocations.append(denomLocation[len(denomLocation)-1])
		for i in range(len(denomLocation)-1):
			listLocations.extend(denomLocation[i].split(','))
		for val in listLocations:
			coordinates=self.getCoordinates(val)
			longitude=coordinates[0]
			latitude=coordinates[1]
			city="Test"
			postalCode=48014
	 		SQLSelect="SELECT id FROM LOCATION WHERE DENOM=%s and lon=%s and lat=%s;"
	 		self.cursor.execute(SQLSelect,(val,longitude,latitude))
			if self.cursor.rowcount==0:
				SQLocation="INSERT INTO location (denom,city,postalcode,lon,lat) VALUES (%s, %s, %s, %s, %s) returning id;"
				self.cursor.execute(SQLocation, (val, city, postalCode,longitude,latitude))
				location_id=self.cursor.fetchone()[0]
			else:
				location_id=self.cursor.fetchone()[0]
			SQLSelectEvent="Select id FROM event WHERE DENOM=%s;"
			self.cursor.execute(SQLSelectEvent,(denomEvent,))
			if self.cursor.rowcount==0:
				SQLEvent="INSERT INTO event (denom, price_anticipada,price, startdate, endate, type_id, information_url) VALUES (%s, %s, %s,%s, %s, %s, %s) returning id;"
				print price_anticipada
				print price
				self.cursor.execute(SQLEvent, (denomEvent,float(price_anticipada), float(price), startDate,endDate,categoryId, information_url))
				event_id=self.cursor.fetchone()[0]
			else:
				event_id=self.cursor.fetchone()[0]
			SQLSelectEventLocation="SELECT location_id FROM EVENT_LOCATION WHERE LOCATION_ID=%s and EVENT_ID=%s;"
			self.cursor.execute(SQLSelectEventLocation,(location_id,event_id))
			if self.cursor.rowcount==0:
				SQLEventLocation="INSERT INTO EVENT_LOCATION (LOCATION_ID,EVENT_ID) VALUES (%s,%s);"
				self.cursor.execute(SQLEventLocation,(location_id,event_id))
 		self.conn.commit()

 	def insertPatrimonioToDB(self, name, category, address, description, informationLink, lon, lat):
		SQLSelect="SELECT id FROM EMBLEMATIC_BUILDING WHERE DENOM_ES=%s;"
 		self.cursor.execute(SQLSelect,(name,))
		if self.cursor.rowcount==0:
 			SQLSelect="SELECT id FROM BUILDING_TYPE WHERE DENOM_ES=%s;"
	 		self.cursor.execute(SQLSelect,(category,))
			if self.cursor.rowcount==0:
				SQLocation="INSERT INTO BUILDING_TYPE (denom_es) VALUES (%s) returning id;"
				self.cursor.execute(SQLocation, (category,))
				category_id=self.cursor.fetchone()[0]
			else:
				category_id=self.cursor.fetchone()[0]
			SQLEvent="INSERT INTO LOCATION (denom, address, geom) VALUES (%s, %s, ST_GeomFromText('POINT(%s %s)', 4326)) returning id;"
			self.cursor.execute(SQLEvent, (name,address,lon,lat))
			location_id=self.cursor.fetchone()[0]
			SQLEvent="INSERT INTO EMBLEMATIC_BUILDING(denom_es,location_id, description_es, information_url, BUILDING_TYPE) VALUES (%s, %s, %s, %s, %s) returning id;"
			self.cursor.execute(SQLEvent, (name,location_id,description,informationLink,category_id))
		self.conn.commit()




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



