# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GeneItem(scrapy.Item):
    GeneName = scrapy.Field()
    GeneID = scrapy.Field()
    GeneURL = scrapy.Field()
    CCDSURL = scrapy.Field()
    CCDS = scrapy.Field()

class CDSItem(scrapy.Item):
    CDSID = scrapy.Field()
    CDSURL = scrapy.Field()
    CDSNT = scrapy.Field()
    CDSAA = scrapy.Field()