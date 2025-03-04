import scrapy
import time
from ..items import StockDividendItem

class StockDividendSpider(scrapy.Spider):
    name = "stock-dividend"
    allowed_domains = ["goodinfo.tw"]
    start_urls = ["https://goodinfo.tw/tw2/StockList.asp?SHEET=%E8%82%A1%E5%88%A9%E6%94%BF%E7%AD%96&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E5%90%88%E8%A8%88%E8%82%A1%E5%88%A9+(%E6%9C%80%E6%96%B0%E5%B9%B4%E5%BA%A6)@@%E5%90%88%E8%A8%88%E8%82%A1%E5%88%A9@@%E6%9C%80%E6%96%B0%E5%B9%B4%E5%BA%A6"]


    def start_requests(self):

        time.sleep(5)
        url = f"https://goodinfo.tw/tw2/StockList.asp?SHEET=%E8%82%A1%E5%88%A9%E6%94%BF%E7%AD%96&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E5%90%88%E8%A8%88%E8%82%A1%E5%88%A9+(%E6%9C%80%E6%96%B0%E5%B9%B4%E5%BA%A6)@@%E5%90%88%E8%A8%88%E8%82%A1%E5%88%A9@@%E6%9C%80%E6%96%B0%E5%B9%B4%E5%BA%A6"
        
        print(f"正在爬取...")
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            headers={
                        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                    },
            cookies=dict(each.split('=', 1) for each in "CLIENT%5FID=20250203223342375%5F220%2E136%2E199%2E67; IS_TOUCH_DEVICE=F; _ga=GA1.1.1164361772.1738593242; TW_STOCK_BROWSE_LIST=2330; SCREEN_SIZE=WIDTH=1536&HEIGHT=864; FCNEC=%5B%5B%22AKsRol_AGAcAdHaKmYZ9-_FSAxn-pqxumG1g3D7ZxQTf8js9LZi-UXZYgxHDw5BYzvwShQ3QArQFbvQuzJKdBNvQmkojf4dqBWO9DFhnE_n2j58twHforgpq6D4au5tV5NGCTO-2RR3HkXnMqGImDEp3bhY3kcPk5Q%3D%3D%22%5D%5D; cto_bundle=5asRHl9WVDNDSjVLNjZ2NkJYcWNQTGFUWmlGVXRjd2hKaUk1NEZjcXBiQkpCbCUyQjhRdDJ3V1cydTdtOFpWRTh1NzFJMUZubWl5WUlVa3VTeEp3eWtaUWtiTHVkUHAwZUtSV1lGV1BNUnQwTXU3cE9NWFgzWXFETmVybFN2NzRPZ05ibWtCbm1JN09EaHlham10UVhaZFJXNkZrUGY3d2tQd1ZTMVlMRGRCNVg3RGlUWDZWUERiN3FnTDN6dm4yZ3l2bk9jU0Q5d0dkeU9lWWdEVnIlMkJVUSUyQnd2RFJ5MWpaMlpuSXh1bm9pU2N3WVpHJTJGQUk2SzdrR2hlTjVRMTdPV2FPZmF4dzg; cto_bidid=qrCHeF9OQ2t2Sm1qWm1IV3hWd2lNR0Z1UmNIU1hCbXNuZkVIaFV2eUw4JTJCRnNPcnZQSWJlOFRoc2lhbFNMV3NvajYlMkZxQ3VDQVFkc1E4NGx3QllSZVU1RGtqWU1OMW5pRlhHN2t5eTJONk0xdURlTTQlM0Q; __gads=ID=0b7edfb8594bd460:T=1738593244:RT=1738752320:S=ALNI_MYM67KAp6soPlatSXAfpl8AjmNUxw; __gpi=UID=0000101e2dc94fbf:T=1738593244:RT=1738752320:S=ALNI_MasWExVvcvOKLcr2s6PbGqB3MlMow; __eoi=ID=331fbbe2fa7e0dbf:T=1738593244:RT=1738752320:S=AA-AfjZkIDtwNxvjCB1NmEva1rIW; cto_bundle=rnamS19WVDNDSjVLNjZ2NkJYcWNQTGFUWmlQRmVXMU1Fc3BVamcyc0RxaW9WTUcybVoxR3NWY3l0ZHlCTlJlSnQ5Q1lBYURWTmdsYXRRSHVCS2FoMXpuVE9KSUJic2p5QnBrRENjZm9abWVaenNOTEVrVDF4R3NQWVBCUTl3QWZzMTIlMkJWdXFTNk95QlVvdEVNZUdvQTU3SDVrcGRJekNBR0xGYWR5U01VbkM3ZXlWSE1ydkR1RDJreXZaUjRFREhJbTNxSG1BR3RqbTc4TUI0dUtoUGpVa1RvU2lvYWM0Q0RaRGc4STMzTiUyQmVZd1BVZ2dscE84UEQxd3pHVFJWaTg5dlNRcw; _ga_0LP5MLQS7E=GS1.1.1738756184.7.0.1738756184.60.0.0".split(";"))
        )


    def parse(self, response):
        titles = []
        for each in response.css("#tblStockList .bg_h2:nth-child(1) > th"):
            title = ''.join(each.css("*::text").getall())
            titles.append(title)
        # print(titles)

        for each in response.css("#tblStockList tr"):
            rows = []

            for td in each.css("tr[id^='row'] td:nth-child(1)"):
                row = td.css("*::text").get()
                rows.append(row)
            
            for th in each.css("tr[id^='row'] th"):
                row = th.css("*::text").get()
                rows.append(row)

            for td in each.css("tr[id^='row'] td"):
                row = td.css("*::text").get()
                rows.append(row)

            if rows == []:
                continue
                
            del rows[3]
            # print()
            # print(rows)
            
        
                  
            stock_dividend = dict(zip(titles, rows))

            stockDividendItem = StockDividendItem()
            stockDividendItem['rank'] = stock_dividend.get('排名')
            stockDividendItem['code'] = stock_dividend.get('代號')
            stockDividendItem['name'] = stock_dividend.get('名稱')
            stockDividendItem['trading_price'] = stock_dividend.get('成交')
            stockDividendItem['dividend_distribution_year'] = stock_dividend.get('股利發放年度')
            stockDividendItem['cash_dividend'] = stock_dividend.get('現金股利')
            stockDividendItem['stock_dividend'] = stock_dividend.get('股票股利')
            stockDividendItem['clean_price'] = stock_dividend.get('除息價')
            stockDividendItem['cash_yield'] = stock_dividend.get('除息價現金殖利率')
            stockDividendItem['stock_yield'] = stock_dividend.get('除權價股票殖利率')
            stockDividendItem['cash_dividend_distribution_date'] = stock_dividend.get('現金股利發放日')

            yield stockDividendItem
