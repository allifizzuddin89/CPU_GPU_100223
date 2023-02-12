import scrapy
import json
#using regex to search common names
import re

class AsusGpu01Spider(scrapy.Spider):
    name = "asus_gpu_0.1"
    # allowed_domains = ["x"]
    # start_urls = ["http://x/"]

    url = 'https://odinapi.asus.com/recent-data/apiv2/SeriesFilterResult?SystemCode=asus&WebsiteCode=my&ProductLevel1Code=motherboards-components&ProductLevel2Code=graphics-cards&PageSize=20&PageIndex={i}&CategoryName=AMD,NVIDIA&SeriesName=&SubSeriesName=&Spec=&SubSpec=&Sort=Recommend&siteID=www&sitelang='

    def start_requests(self):
        # pageindex 1 to 10
        for i in range(1,11):
            yield scrapy.Request(
                url=self.url.format(i=i),
                method='GET',
                dont_filter=True,
                callback=self.parse
            )

    def parse(self, response):
        raw_data = response.text
        data = json.loads(raw_data)
        data = data['Result']['ProductList']
        for i in range(0,len(data)):
            item = {
                'Item Name' : 'ASUS '+data[i]['Name'].strip('<h2>').strip('</h2>'),
                'Part No' : data[i]['PartNo'],
                'Manufacturer URL' : data[i]['ProductURL'],
            }
            yield item
