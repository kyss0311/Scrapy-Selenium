# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class FunnowScraperItem(scrapy.Item):
    title = scrapy.Field()  # 名稱
    price = scrapy.Field()  # 價格
    star = scrapy.Field()  # 星星數
    people = scrapy.Field()  # 評論人數
    earliest_datetime = scrapy.Field()  # 最早可訂時間
    link = scrapy.Field()  # 連結
    product_info = scrapy.Field()  # 產品介紹
    product_address = scrapy.Field()  # 地址

class ProductInfoItem(scrapy.Item):
    title = scrapy.Field()  # 名稱
    lowest_option_price = scrapy.Field()  # 最低價格
    option_info = scrapy.Field()  # 產品介紹
    option_star = scrapy.Field()  # 星數
    option_people = scrapy.Field()  # 評論人數
    option_datetime = scrapy.Field()  # 最早可訂時間

