# Scrapy settings for demo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'demo'
SPIDER_MODULES = ['demo.spiders']
NEWSPIDER_MODULE = 'demo.spiders'
ITEM_PIPELINES = ['demo.pipelines.MyImagesPipeline','demo.pipelines.EventPipeline']
IMAGES_STORE = '/users/aritzbi/Development/XploreBilbao/app/images'
LOG_LEVEL='ERROR'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'demo (+http://www.yourdomain.com)'
