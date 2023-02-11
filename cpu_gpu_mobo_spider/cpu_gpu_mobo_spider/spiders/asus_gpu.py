import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_playwright.page import PageMethod


class AsusGpuSpider(CrawlSpider):
    name = 'asus_gpu'
    allowed_domains = ['asus.com']
    # start_urls = ['http://x/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    # def parse_item(self, response):
    #     item = {}
    #     #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    #     #item['name'] = response.xpath('//div[@id="name"]').get()
    #     #item['description'] = response.xpath('//div[@id="description"]').get()
    #     return item

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.asus.com/my/motherboards-components/graphics-cards/all-series/filter?Category=AMD,NVIDIA",
            meta={
                "playwright": True,
                "playwright_page_methods":[
                    ##scrolling until item 189th, least efficient
                    #PageMethod("wait_for_selector"."div.filter_product_list:nth-child(189)"),
                    ##injecting javascript until the end of the page
                    PageMethod("evaluate","window.scrollBy(0,document.body.scrollHeight)"),
                ]
            },
        )