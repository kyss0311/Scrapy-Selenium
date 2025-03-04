# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KkdayScraperItem(scrapy.Item):
    title = scrapy.Field()  # 行程名稱
    link = scrapy.Field()  # 超連結
    tag = scrapy.Field()  # 標籤
    rate = scrapy.Field()  # 評分
    vote_number = scrapy.Field()  # 評分人數
    order_number = scrapy.Field()  # 下訂人數
    price = scrapy.Field()  # 價格
    product_info = scrapy.Field()  # 行程內文的介紹
    options = scrapy.Field()  # 選擇方案
