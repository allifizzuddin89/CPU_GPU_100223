import scrapy


class AsusMoboSpider(scrapy.Spider):
    name = "asus_mobo"
    allowed_domains = ["x"]
    start_urls = ["http://x/"]

    def parse(self, response):
        pass
