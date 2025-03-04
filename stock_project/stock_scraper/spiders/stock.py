import scrapy
import time
from ..items import StockScraperItem 

class StockSpider(scrapy.Spider):
    
    name = "stock"
    allowed_domains = ["goodinfo.tw"]
    start_urls = ["https://goodinfo.tw/tw/index.asp"]
    stockId_list = ['2330','2440'] 
    header = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    Your_cookies = {
                'cookie':"CLIENT%5FID=20250203223342375%5F220%2E136%2E199%2E67; IS_TOUCH_DEVICE=F; _ga=GA1.1.1164361772.1738593242; TW_STOCK_BROWSE_LIST=2330; SCREEN_SIZE=WIDTH=1536&HEIGHT=864; FCNEC=%5B%5B%22AKsRol_AGAcAdHaKmYZ9-_FSAxn-pqxumG1g3D7ZxQTf8js9LZi-UXZYgxHDw5BYzvwShQ3QArQFbvQuzJKdBNvQmkojf4dqBWO9DFhnE_n2j58twHforgpq6D4au5tV5NGCTO-2RR3HkXnMqGImDEp3bhY3kcPk5Q%3D%3D%22%5D%5D; cto_bundle=5asRHl9WVDNDSjVLNjZ2NkJYcWNQTGFUWmlGVXRjd2hKaUk1NEZjcXBiQkpCbCUyQjhRdDJ3V1cydTdtOFpWRTh1NzFJMUZubWl5WUlVa3VTeEp3eWtaUWtiTHVkUHAwZUtSV1lGV1BNUnQwTXU3cE9NWFgzWXFETmVybFN2NzRPZ05ibWtCbm1JN09EaHlham10UVhaZFJXNkZrUGY3d2tQd1ZTMVlMRGRCNVg3RGlUWDZWUERiN3FnTDN6dm4yZ3l2bk9jU0Q5d0dkeU9lWWdEVnIlMkJVUSUyQnd2RFJ5MWpaMlpuSXh1bm9pU2N3WVpHJTJGQUk2SzdrR2hlTjVRMTdPV2FPZmF4dzg; cto_bidid=qrCHeF9OQ2t2Sm1qWm1IV3hWd2lNR0Z1UmNIU1hCbXNuZkVIaFV2eUw4JTJCRnNPcnZQSWJlOFRoc2lhbFNMV3NvajYlMkZxQ3VDQVFkc1E4NGx3QllSZVU1RGtqWU1OMW5pRlhHN2t5eTJONk0xdURlTTQlM0Q; __gads=ID=0b7edfb8594bd460:T=1738593244:RT=1738752320:S=ALNI_MYM67KAp6soPlatSXAfpl8AjmNUxw; __gpi=UID=0000101e2dc94fbf:T=1738593244:RT=1738752320:S=ALNI_MasWExVvcvOKLcr2s6PbGqB3MlMow; __eoi=ID=331fbbe2fa7e0dbf:T=1738593244:RT=1738752320:S=AA-AfjZkIDtwNxvjCB1NmEva1rIW; cto_bundle=rnamS19WVDNDSjVLNjZ2NkJYcWNQTGFUWmlQRmVXMU1Fc3BVamcyc0RxaW9WTUcybVoxR3NWY3l0ZHlCTlJlSnQ5Q1lBYURWTmdsYXRRSHVCS2FoMXpuVE9KSUJic2p5QnBrRENjZm9abWVaenNOTEVrVDF4R3NQWVBCUTl3QWZzMTIlMkJWdXFTNk95QlVvdEVNZUdvQTU3SDVrcGRJekNBR0xGYWR5U01VbkM3ZXlWSE1ydkR1RDJreXZaUjRFREhJbTNxSG1BR3RqbTc4TUI0dUtoUGpVa1RvU2lvYWM0Q0RaRGc4STMzTiUyQmVZd1BVZ2dscE84UEQxd3pHVFJWaTg5dlNRcw; _ga_0LP5MLQS7E=GS1.1.1738756184.7.0.1738756184.60.0.0"
    }

    def start_requests(self):
        for stockId in self.stockId_list:
            time.sleep(5)
            url = f"https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID={stockId}"
            
            print(f"爬取{stockId}...")
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers={
                            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                        },
                cookies=dict(each.split('=', 1) for each in "CLIENT%5FID=20250203223342375%5F220%2E136%2E199%2E67; IS_TOUCH_DEVICE=F; _ga=GA1.1.1164361772.1738593242; TW_STOCK_BROWSE_LIST=2330; SCREEN_SIZE=WIDTH=1536&HEIGHT=864; FCNEC=%5B%5B%22AKsRol_AGAcAdHaKmYZ9-_FSAxn-pqxumG1g3D7ZxQTf8js9LZi-UXZYgxHDw5BYzvwShQ3QArQFbvQuzJKdBNvQmkojf4dqBWO9DFhnE_n2j58twHforgpq6D4au5tV5NGCTO-2RR3HkXnMqGImDEp3bhY3kcPk5Q%3D%3D%22%5D%5D; cto_bundle=5asRHl9WVDNDSjVLNjZ2NkJYcWNQTGFUWmlGVXRjd2hKaUk1NEZjcXBiQkpCbCUyQjhRdDJ3V1cydTdtOFpWRTh1NzFJMUZubWl5WUlVa3VTeEp3eWtaUWtiTHVkUHAwZUtSV1lGV1BNUnQwTXU3cE9NWFgzWXFETmVybFN2NzRPZ05ibWtCbm1JN09EaHlham10UVhaZFJXNkZrUGY3d2tQd1ZTMVlMRGRCNVg3RGlUWDZWUERiN3FnTDN6dm4yZ3l2bk9jU0Q5d0dkeU9lWWdEVnIlMkJVUSUyQnd2RFJ5MWpaMlpuSXh1bm9pU2N3WVpHJTJGQUk2SzdrR2hlTjVRMTdPV2FPZmF4dzg; cto_bidid=qrCHeF9OQ2t2Sm1qWm1IV3hWd2lNR0Z1UmNIU1hCbXNuZkVIaFV2eUw4JTJCRnNPcnZQSWJlOFRoc2lhbFNMV3NvajYlMkZxQ3VDQVFkc1E4NGx3QllSZVU1RGtqWU1OMW5pRlhHN2t5eTJONk0xdURlTTQlM0Q; __gads=ID=0b7edfb8594bd460:T=1738593244:RT=1738752320:S=ALNI_MYM67KAp6soPlatSXAfpl8AjmNUxw; __gpi=UID=0000101e2dc94fbf:T=1738593244:RT=1738752320:S=ALNI_MasWExVvcvOKLcr2s6PbGqB3MlMow; __eoi=ID=331fbbe2fa7e0dbf:T=1738593244:RT=1738752320:S=AA-AfjZkIDtwNxvjCB1NmEva1rIW; cto_bundle=rnamS19WVDNDSjVLNjZ2NkJYcWNQTGFUWmlQRmVXMU1Fc3BVamcyc0RxaW9WTUcybVoxR3NWY3l0ZHlCTlJlSnQ5Q1lBYURWTmdsYXRRSHVCS2FoMXpuVE9KSUJic2p5QnBrRENjZm9abWVaenNOTEVrVDF4R3NQWVBCUTl3QWZzMTIlMkJWdXFTNk95QlVvdEVNZUdvQTU3SDVrcGRJekNBR0xGYWR5U01VbkM3ZXlWSE1ydkR1RDJreXZaUjRFREhJbTNxSG1BR3RqbTc4TUI0dUtoUGpVa1RvU2lvYWM0Q0RaRGc4STMzTiUyQmVZd1BVZ2dscE84UEQxd3pHVFJWaTg5dlNRcw; _ga_0LP5MLQS7E=GS1.1.1738756184.7.0.1738756184.60.0.0".split(";"))
            )
            

    def parse(self, response):
        stockScraperItem = StockScraperItem()

        stock_name = response.css("table.b0v1h0.p4_2 tr.bg_h0 nobr:nth-child(1) a::text").get()
        date = response.css("table.b0v1h0.p4_2 tr.bg_h0 nobr:nth-last-child(1)::text").get()
        table_titles = response.css("table.b0v1h0.p4_2 tr.bg_h1 th nobr::text").getall()
        table_vaules = response.css("table.b0v1h0.p4_2 tr.bg_h1 + tr td *::text").getall()

        info = {}
        if len(table_titles) == len(table_vaules):
            for i in range(len(table_titles)):
                title = table_titles[i]
                value = table_vaules[i]
                info[title] = value
        else:
            print("The number of title and value in the table doesn't match")

        stockScraperItem['stock_name'] = stock_name
        stockScraperItem['date'] = date
        stockScraperItem['deal_price'] = info.get('成交價')
        stockScraperItem['opening_price'] = info.get('開盤')
        stockScraperItem['closing_price'] = info.get('昨收')
        stockScraperItem['highest_price'] = info.get('最高')
        stockScraperItem['lowest_price'] = info.get('最低')

        yield stockScraperItem
      