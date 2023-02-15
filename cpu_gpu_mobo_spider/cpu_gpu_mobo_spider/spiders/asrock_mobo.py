import scrapy
import pandas as pd


class AsrockMoboSpider(scrapy.Spider):
    name = "asrock_mobo"
    url ="https://www.asrock.com/support/cpu.us.asp?s={}"

    def start_requests(self):
        cpu_socket = list("AM3","AM4","SP3","TR4","R4","LGA 1200","LGA 1155","LGA 1151","LGA 1156","LGA 2011","FM1","AM3+","LGA 1366","LGA 3647","LGA 2066","LGA 4189","LGA 1150","LGA 1700","LGA1700","AM5","SP5","LGA 4677","LGA 1567","LGA 771","AM2","AM2+")
        
        # for url in self.start_urls:
        for i in cpu_socket:
            if i != None:
                yield scrapy.Request(
                    url=self.url.format(i), 
                    headers= {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42"},
                    # free rotating proxy webshare
                    # please kindly register for paid proxy if you require to run this code without disruption
                    meta = {"proxy" : "http://wojlycot-rotate:gow56st01xs6@p.webshare.io:80"},
                    dont_filter=True, 
                    cb_kwargs={'cpusocket':i} ,
                    callback=self.parse
                    )

    def parse(self, response, year, cpusocket):
        dfs = pd.read_html(response.css('div.wide-80-1.right.Support > table').get())
        df = pd.concat(dfs)
        yield df.head()
        # df = df.iloc[:,[0,2,4,8]]
        # df.to_csv('ASROCK_mobo_{}.csv'.format(cpusocket))