# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import psycopg2
from pygeocoder import Geocoder
import pprint
import datetime;

class DemoPipeline(object):
    def process_item(self, item, spider):
    	print 'asdasdasda'
        return item

class EventPipeline(object):
	def __init__(self):
		print 'Init del event pipeline'
		conn_string = "host='localhost' dbname='mydb' user='doctor' password='who'"
		# print the connection string we will use to connect
		print "Connecting to database\n	->%s" % (conn_string)
		# get a connection, if a connect cannot be made an exception will be raised here
		self.conn = psycopg2.connect(conn_string)
		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		self.cursor = self.conn.cursor()
	def process_item(self,item,spider):
		if spider.name == 'bilbao_spider':
			denomLocation=item['location']
			denomEvent=item['title']
			#price=item['price']
			startDate=item['startDate'][0]
			startDate=startDate.split('-')
			endDate=item['endDate'][0]
			endDate=endDate.split('-')
			if(len(denomLocation)!=0):
				self.insertDataToDB(denomLocation[0], denomEvent[0],1,startDate,endDate)
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
			self.insertDataToDB(item['location'][0],item ['title'][0],5,startDate,endDate)
			#'Category: '+ item ['category'][0]


	def insertDataToDB(self, denomLocation, denomEvent, price, startDate, endDate):
		denomLocation=denomLocation.split('y')
		listLocations=[]
		listLocations.append(denomLocation[len(denomLocation)-1])
		for i in range(len(denomLocation)-1):
			listLocations.extend(denomLocation[i].split(','))
		for val in listLocations:
			try:
	 			results=Geocoder.geocode(val)
			except: 
				print 'Lugar del fallo: '+val
			coordinates=results[0].coordinates
			longitude=coordinates[0]
			latitude=coordinates[1]
			city=results[0].city
			postalCode=results[0].postal_code

	 		SQLSelect="SELECT id FROM LOCATION WHERE DENOM=%s and long=%s and lat=%s;"
	 		self.cursor.execute(SQLSelect,(val,longitude,latitude))
			if self.cursor.rowcount==0:
				SQLocation="INSERT INTO location (denom,city,postalcode,long,lat) VALUES (%s, %s, %s, %s, %s) returning id;"
				self.cursor.execute(SQLocation, (val, city, postalCode,longitude,latitude))
				location_id=self.cursor.fetchone()[0]
			else:
				location_id=self.cursor.fetchone()[0]
			SQLSelectEvent="Select id FROM event WHERE DENOM=%s;"
			self.cursor.execute(SQLSelectEvent,(denomEvent,))
			if self.cursor.rowcount==0:
				SQLEvent="INSERT INTO event (denom, price, startdate, endate) VALUES (%s, %s, %s, %s) returning id;"
				self.cursor.execute(SQLEvent, (denomEvent, price, startDate,endDate))
				event_id=self.cursor.fetchone()[0]
			else:
				event_id=self.cursor.fetchone()[0]
			SQLSelectEventLocation="SELECT location_id FROM EVENT_LOCATION WHERE LOCATION_ID=%s and EVENT_ID=%s;"
			self.cursor.execute(SQLSelectEventLocation,(location_id,event_id))
			if self.cursor.rowcount==0:
				SQLEventLocation="INSERT INTO EVENT_LOCATION (LOCATION_ID,EVENT_ID) VALUES (%s,%s);"
				self.cursor.execute(SQLEventLocation,(location_id,event_id))
 		self.conn.commit()
