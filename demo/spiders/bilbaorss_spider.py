from scrapy.spider import Spider 
from scrapy.selector import HtmlXPathSelector 
from scrapy.http.request import Request
from scrapy.selector import Selector
from demo.items import BilbaoItem
import datetime

class BilbaoRSSSpider(Spider):
	BASE=''
	name='bilbaorss_spider'