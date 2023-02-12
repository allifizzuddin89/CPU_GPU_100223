import scrapy

class asusmobo(scrapy.Item):
    item_name = scrapy.Field()
    link = scrapy.Field()

class asusgpu(scrapy.Item):
    item_name = scrapy.Field()
    link = scrapy.Field()