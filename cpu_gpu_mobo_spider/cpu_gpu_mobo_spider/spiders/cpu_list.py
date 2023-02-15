import scrapy
import pandas as pd
import json
from creds import API
from scraper_api import ScraperAPIClient
client = ScraperAPIClient(API)

class CpuListSpider(scrapy.Spider):
    name = "cpu_list"
    allowed_domains = ["techpowerup.com"]
    # start_urls = ["https://www.techpowerup.com/cpu-specs/?mfgr={0}&released={1}&sort=name"]

    url ="https://www.techpowerup.com/cpu-specs/?mfgr={0}&released={1}&sort=name"
    # url = "https://httpbin.org/ip"

    def start_requests(self):
        cpu_manu = ['AMD', 'Intel']
        year = [2019, 2020, 2021, 2022, 2023]
        # for url in self.start_urls:
        for i in cpu_manu:
            for j in year:
                yield scrapy.Request(
                    url=self.url.format(i,j), 
                    headers= {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42"},
                    meta = {"proxy" : "http://wojlycot-rotate:gow56st01xs6@p.webshare.io:80"},
                    dont_filter=True, 
                    cb_kwargs={'year':j, 'manu':i} ,
                    callback=self.parse
                    )
                
                # yield scrapy.Request(client.scrapyGet(url=self.url.format(i,j)), dont_filter=True, cb_kwargs={'year':j, 'manu':i} ,callback=self.parse)

    def parse(self, response, year, manu):
        dfs = pd.read_html(response.css('table.processors').get())
        df = pd.concat(dfs)
        df.to_csv('CPU_List_{0}_{1}.csv'.format(manu,year))

        # df = dfs.tail(-1)
        # for k, df in enumerate(dfs):
            # df.columns = df.iloc[1]
            # df = df[1:]
            # df1 = df.drop(df.columns[[1,3,5,6,7,8]]).copy(deep=True)
            # # working but only in ranges
            # df = df.iloc[:,[0:-1]].reset_index(drop=True)
            # print('\n\n{}\n\n'.format(df[1]))
            # df.insert(len(df.columns), 'Manufacturing', manu)

            # ## delete multiindex column
            # df.columns = df.iloc[0]
            # ## reset the index, perhaps not needed in this case but as precaution only
            # df = df.iloc[1:].reset_index(drop=True)
            # df = df.iloc[:,[0,1]]
            # print(df.head())

            # df.drop(index=0)
            # df.drop(columns=df.columns[1,2,4,5,6], axis=1, inplace=True)
            # df.drop(df.iloc[:,[0,2,4,9]], inplace=True)
            # df = df[[0,2,4,6,7,8,10]]
            # df = df.iloc[1:,[1,3]].reset_index(drop=True)
            # df.drop(df.index[0], inplace=True)
            # df.drop(df.columns[[0,2,4,6,7,8,10]], axis=1, inplace=True)
            # new_column = ['Name', 'Codename', 'Cores', 'Socket', 'Released Year']
            # df = df[new_column]
            # df['Manufacturer'] = manu
            # print(list(df.columns))
            # col_name = [row[i] for row in list(df.columns) for i in range(2)]
            # col_name = [x for x in df.columns[0] if x == 'Intel' if x == 'AMD']
            # print('\n\n\{}\n\n').format(col_name)
            # for y in range(0,2):
            # print(type(df.columns))
            # print(df.head().to_markdown())
            # df.to_csv('CPU_List_{0}_{1}.csv'.format(manu,year)) 
