import scrapy
from items import asusmobo


class AsusMoboSpider(scrapy.Spider):
    name = "asus_mobo"
    # allowed_domains = ["x"]
    # start_urls = ["http://x/"]

    def start_requests(self):
        url = "https://www.asus.com/my/motherboards-components/motherboards/all-series/filter?Category=Intel,AMD"
        yield scrapy.Request(url, meta={'playwright': True})
    
    def parse(self, response):
        for mobo in response.css('div.filter_product_list'):
            mobo_item = asusmobo()
            mobo_item['item_name'] : mobo.css('a[href]>h2::text').get()
            mobo_item['link'] : mobo.css('a[href^="https://"]:nth-child(7)')
