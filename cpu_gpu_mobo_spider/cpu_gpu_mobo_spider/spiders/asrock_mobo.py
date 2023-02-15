import scrapy
import pandas as pd
import urllib.parse


class AsrockMoboSpider(scrapy.Spider):
    name = "asrock_mobo"
    url ="https://www.asrock.com/support/cpu.us.asp?s={}"

    def start_requests(self):
        # cpu_socket = ["AM3","AM4","SP3","TR4","R4","LGA 1200","LGA 1155","LGA 1151","LGA 1156","LGA 2011","FM1","AM3+","LGA 1366","LGA 3647","LGA 2066","LGA 4189","LGA 1150","LGA 1700","LGA1700","AM5","SP5","LGA 4677","LGA 1567","LGA 771","AM2","AM2+"]
        cpu_socket = ["AM4", "1200", "2066", "2011", "1700", "1156", "1155", "1151", "1150", "sTRX4", "TR4", "AM5", "FM2%2b", "FM2", "FM1", "AM3%2b", "AM1"]
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

    def parse(self, response, cpusocket):
        # if cpusocket != "FM2%2b" and cpusocket != "AM3%2b":
        dfs = pd.read_html(response.css('div.wide-80-1.right.Support > table').get())
        df = pd.concat(dfs)
        df = df.iloc[:,:-1]
        df['Manufacturer'] = 'ASROCK'
        df['CPU Socket'] = cpusocket
        cols = df.columns.tolist()
        cols = cols[-2:] + cols[:-2]
        df = df[cols]
        # df[['CPU Chipset','Part number']] = df.Model.str.split('\(|\)', expand=True)
        # item = df.head()
        # print(item)
        df.to_csv('ASROCK_mobo_{}.csv'.format(cpusocket))
        # elif cpusocket == "FM2%2b":
        #     i = cpusocket.index('FM2%2b')
        #     cpusocket[i] = cpusocket[i].encode('utf8')
        #     dfs = pd.read_html(response.css('div.wide-80-1.right.Support > table').get())
        #     df = pd.concat(dfs)
        #     df = df.iloc[:,:-1]
        #     df['Manufacturer'] = 'ASROCK'
        #     df['CPU Socket'] = cpusocket
        #     cols = df.columns.tolist()
        #     cols = cols[-2:] + cols[:-2]
        #     df = df[cols]
        #     # df[['CPU Chipset','Part number']] = df.Model.str.split('\(|\)', expand=True)
        #     item = df.head()
        #     print(item)
        #     # df.to_csv('ASROCK_mobo_{}.csv'.format(cpusocket))
        # elif cpusocket == "FM3%2b":
        #     i = cpusocket.index('FM3%2b')
        #     cpusocket[i] = cpusocket[i].encode('utf8')
        #     dfs = pd.read_html(response.css('div.wide-80-1.right.Support > table').get())
        #     df = pd.concat(dfs)
        #     df = df.iloc[:,:-1]
        #     df['Manufacturer'] = 'ASROCK'
        #     df['CPU Socket'] = cpusocket
        #     cols = df.columns.tolist()
        #     cols = cols[-2:] + cols[:-2]
        #     df = df[cols]
        #     # df[['CPU Chipset','Part number']] = df.Model.str.split('\(|\)', expand=True)
        #     item = df.head()
        #     print(item)
        #     # df.to_csv('ASROCK_mobo_{}.csv'.format(cpusocket))
