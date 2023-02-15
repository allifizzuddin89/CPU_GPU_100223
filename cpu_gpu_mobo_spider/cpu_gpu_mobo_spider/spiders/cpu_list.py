import scrapy
import pandas as pd

class CpuListSpider(scrapy.Spider):
    name = "cpu_list"
    allowed_domains = ["techpowerup.com"]
    url ="https://www.techpowerup.com/cpu-specs/?mfgr={0}&released={1}&sort=name"

    def start_requests(self):
        cpu_manu = ['AMD', 'Intel']
        year = [2019, 2020, 2021, 2022, 2023]
        # for url in self.start_urls:
        for i in cpu_manu:
            for j in year:
                yield scrapy.Request(
                    url=self.url.format(i,j), 
                    headers= {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42"},
                    # free rotating proxy webshare
                    # please kindly register for paid proxy if you require to run this code without disruption
                    meta = {"proxy" : "http://wojlycot-rotate:gow56st01xs6@p.webshare.io:80"},
                    dont_filter=True, 
                    cb_kwargs={'year':j, 'manu':i} ,
                    callback=self.parse
                    )

    def parse(self, response, year, manu):
        dfs = pd.read_html(response.css('table.processors').get())
        df = pd.concat(dfs)
        df = df.iloc[:,[0,2,4,8]]
        df.to_csv('CPU_List_{0}_{1}.csv'.format(manu,year))