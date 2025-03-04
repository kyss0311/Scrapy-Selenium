# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockScraperItem(scrapy.Item):
    stock_name = scrapy.Field()  #股票名稱(stock_name)
    date = scrapy.Field()  # 日期(date)
    deal_price = scrapy.Field()  # 成交價(deal_price)
    opening_price = scrapy.Field()  # 開盤價(opening_price)
    closing_price = scrapy.Field()  # 收盤價(closing_price)
    highest_price = scrapy.Field()  # 最高價(highest_price)
    lowest_price = scrapy.Field()  # 最低價(lowest_price)
   
class StockDividendItem(scrapy.Item):
    rank = scrapy.Field() # 排名(rank)
    code = scrapy.Field() # 代號(code)
    name = scrapy.Field() # 名稱(name)
    trading_price = scrapy.Field() # 成交(trading_price)
    dividend_distribution_year = scrapy.Field()  # 股利發放年度 (dividend_distribution_year)
    EPS = scrapy.Field() # 所屬EPS(EPS)
    cash_dividend = scrapy.Field() # 現金股利(cash_dividend)
    stock_dividend = scrapy.Field() # 股票股利(stock_dividend)
    clean_price = scrapy.Field() # 除息價(clean_price)
    cash_yield = scrapy.Field() # 現金殖利率(cash_yield)
    stock_yield = scrapy.Field()  # 股票殖利率(stock_yield)
    cash_dividend_distribution_date = scrapy.Field() # 現金股利發放日(cash_dividend_distribution_date)
