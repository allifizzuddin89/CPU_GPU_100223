import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector


class AsusGpuSpider(CrawlSpider):
    name = 'asus_gpu'
    # allowed_domains = ['asus.com']
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
        # yield scrapy.Request(
        #     url="https://www.asus.com/my/motherboards-components/graphics-cards/all-series/filter?Category=AMD,NVIDIA",
        #     meta={
        #         "playwright": True,
        #         #calling object, more efficient
        #         "playwright_page_methods":[
        #             #scrolling until item 189th, least efficient
        #             # PageMethod("wait_for_selector","div.filter_product_list:nth-child(20)"),
        #             # #injecting javascript until the end of the page
        #             # PageMethod("evaluate","window.scrollBy(0,document.body.scrollHeight)"),
        #             # PageMethod("wait_for_selector","div.filter_product_list:nth-child(20)"),
        #             # PageMethod("evaluate","window.scrollBy(0,document.body.scrollHeight)"),
        #             # #and so on, goes on, least efficient
        #             PageMethod("wait_for_selector","div.filter_product_list"),
        #         ],
        #         "playwright_include_page":True,
        #     },
        #     errback = self.close_page,
        # )
        yield scrapy.Request(
            url="https://www.asus.com/my/motherboards-components/graphics-cards/all-series/filter?Category=AMD,NVIDIA",
            meta = dict(
                playwright = True,
                playwright_include_page = True,
                playwright_page_method = [
                    PageMethod('wait_for_selector', 'div.filter_product_list'),
                ],
                errback = self.close_page
            )
        )

        async def parse(self, response):
            # this chunk is meant for downloading java loaded webpage
            # playwright_page download request
            page = response.meta["playwright_page"]
            # scrolling page
            await page.evaluate("window.scrollBy(0,document.body.scrollHeight)")
            await page.wait_for_selector('div.filter_product_list')
            html = await page.content()
            # scrapy style selector?
            s  = Selector(text=await page.content())
            await page.close()

            # for gpu in response.css(div.filter_product_list):
            for gpu in s.css('div.LevelThreeFilterPage__productListTemplate__Qnsre'):
                yield {
                    'Item Name': gpu.css('div.filter_product_list>a[href]>h2 ::text').get(),
                    'Link to manufacture': gpu.css('div.filter_product_list > a[href*="https://www.asus.com/my/Motherboards-Components/Graphics-Cards/"]:last-child::text').get(),
                }       

        # close page, else memory usage piling up even after closed
        async def close_page(self, failure):
            page = failure.request.meta["playwright_page"]
            await page.close()