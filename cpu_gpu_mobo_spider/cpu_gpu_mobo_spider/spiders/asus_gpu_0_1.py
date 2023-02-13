import scrapy
import json
# To remove duplicate string
from collections import OrderedDict
#using regex for housekeeping
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
        
        def removeduplicate(str):
            return "".join(OrderedDict.fromkeys(str))

        for i in range(0,len(data)):
            cleanup = re.compile(r'<h2>|</h2>|</br>')
            item_name = cleanup.sub('','ASUS '+data[i]['Name'])
            # print(f'\n{item_name}\n')
            item = {
                'Item Name' : item_name,
                'Part No' : data[i]['PartNo'],
                'Manufacturer URL' : data[i]['ProductURL'],
            }
            yield item
