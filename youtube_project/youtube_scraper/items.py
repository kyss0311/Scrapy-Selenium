# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeScraperItem(scrapy.Item):
    title = scrapy.Field()  # 影片標題
    link = scrapy.Field()  # 影片超連結
    channel = scrapy.Field()  # 頻道
    view = scrapy.Field()  # 觀看次數
    duration = scrapy.Field()  # 歷經時間
    keywords = scrapy.Field()  # 關鍵字
