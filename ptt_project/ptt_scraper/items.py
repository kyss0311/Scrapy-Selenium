# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# 要將擷取到的資訊封裝成item
import scrapy


class ArticleItem(scrapy.Item):
    article_id = scrapy.Field() # 文章的id
    push = scrapy.Field() # 文章推文數量
    title = scrapy.Field() # 文章標題
    link = scrapy.Field() # 文章超連結
    author = scrapy.Field() # 文章作者
    published_date = scrapy.Field() # po文日期
    content = scrapy.Field() # 內文 


class CommentItem(scrapy.Item):
    article_id = scrapy.Field() # 文章id
    push_tag = scrapy.Field() # 留言的推文數量
    push_user_id = scrapy.Field() # 留言者id
    push_content = scrapy.Field() # 留言內文
    push_ipdatetime = scrapy.Field() # 留言的ip時間日期