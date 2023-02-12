import scrapy
import json
#using regex to search common names
import re

import logging
logger = logging.getLogger('my_logger')
# logging.warning("This is a warning")
logging.basicConfig(filename="logfile.txt", 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    filemode='w',
                    level = logging.DEBUG)

class AsusMoboSpider(scrapy.Spider):
    name = "asus_mobo"

    url = 'https://odinapi.asus.com/recent-data/apiv2/SeriesFilterResult?SystemCode=asus&WebsiteCode=my&ProductLevel1Code=motherboards-components&ProductLevel2Code=motherboards&PageSize=20&PageIndex={i}&CategoryName=Intel,AMD&SeriesName=&SubSeriesName=&Spec=&SubSpec=&Sort=Recommend&siteID=www&sitelang='

    headers = {
        "authority": "odinapi.asus.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ms;q=0.8,id;q=0.7",
        "dnt": "1",
        "origin": "https://www.asus.com",
        "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41"
    }


    def start_requests(self):
        for i in range(1,11):
            yield scrapy.Request(
                url=self.url.format(i=i),
                method='GET',
                dont_filter=True,
                headers=self.headers,
                callback=self.parse
            )
    
    def parse(self, response):
        cpu_socket = re.compile(r'AM3|AM4|SP3|TR4|R4|LGA 1200|LGA 1155|LGA 1151|LGA 1156|LGA 2011|FM1|AM3+|LGA 1366|LGA 3647|LGA 2066|LGA 4189|LGA 1150|LGA 1700|LGA1700|AM5|SP5|LGA 4677|LGA 1567|LGA 771|AM2|AM2+')
        mobo_chipset = re.compile(r'H55|P55|H57|Q57|H61|B65|P67|H67|Q67|Z68|B75|Q75|Z75|H77|Q77|Z77|H81|B85|Q85|Q87|H87|Z87|Z97|H97|X58|X79|X99|H110|B150|Q150|H170|Q170|Z170|B250|Q250|H270|Q270|Z270|Z370|H310|B360|B365|H370|Q370|Z390|C232|C236|C242|C246|H370|Q370|Z390|H410|B460|H470|Q470|Z490|W480|H420E|Q470E|W480E|H510|B560|H570|Z590|W580|Z690|W680|Q670|H670|B660|H610|R680E|Q670E|H610E|Z790|H770|B760|A300|X300|Pro 500|A320|B350|X370|B450|X470|A520|B550[h]|X570|X399|TRX40|WRX80|A620|B650|B650E|X670|X670E')
        raw_data = response.text
        data = json.loads(raw_data)
        data = data['Result']['ProductList']
        for i in range(0,len(data)):
            cpu = cpu_socket.search(data[i]['ModelSpec'])
            mobo = mobo_chipset.search(data[i]['ModelSpec'])
            if (cpu != None and mobo != None):
                item = {
                    'Item Name' : 'ASUS '+data[i]['Name'].strip('<h2>').strip('</h2>'),
                    'Part No' : data[i]['PartNo'],
                    'CPU Socket' : cpu.group(),
                    'Chipset' :mobo.group(),
                    'Manufacturer URL' : data[i]['ProductURL'],
                }
                yield item