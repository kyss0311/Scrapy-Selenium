import scrapy
import re
# 引入封裝模型
from .. items import ArticleItem,CommentItem

class PttSpider(scrapy.Spider):  # 繼承 scrapy.Spider
    ROOT_URL = "https://www.ptt.cc"
    PAGE_LIMIT = 3
    current_page = 1
    board = 'Gossiping'


    name = 'ptt'
    allowed_domains = ['www.ptt.cc']
    start_urls = [f'https://www.ptt.cc/bbs/{board}/index.html']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cookies={'over18': '1'}
            )
      

    def parse(self, response):
        print(f"Scraping the page {self.current_page}...")
        # 爬取當前頁面
        yield from self.__parse_article_list(response)

        # 爬取下一頁
        if self.current_page < self.PAGE_LIMIT:
            yield from self.__paese_next_page(response)

    def __paese_next_page(self, response):
        buttons = response.css("a.btn.wide::text").getall()
        
        if buttons != [] and buttons[1] == "‹ 上頁":
            next_page_url = self.ROOT_URL + response.css("a.btn.wide::attr(href)").getall()[1]
            self.current_page += 1
            yield scrapy.Request(
                url = next_page_url,
                callback = self.parse               
            )



    def __parse_article_list(self, response):
        # response.xpath().get()
        # print(response.css(".title > a::text").get())
        # self.logger.debug("This is a DEBUG level log") 
        # self.logger.info("This is a INFO level log") 
        # self.logger.warning("This is a WARNING level log") 
        # self.logger.error("This is a ERROR level log") 
        # self.logger.critical("This is a CRITICAL level log")

        for each in response.css('.r-ent'):
            link = each.css(".title > a::attr(href)").get()
            if link is None:
                continue
  

            regex_pattern = r"\/bbs\/"+ self.board + r"\/([A-z]{1}\.[0-9]*\.[A-z]{1}\.[A-z0-9]+)\.html$"
            _res = re.match(regex_pattern, link)
            if _res is not None:
                article_id = _res[1]
            else:
                continue
           
            push = each.css("div.nrec > span::text").get()
            title = each.css(".title > a::text").get()
            link = self.ROOT_URL + link
            author = each.css("div.meta > div.author::text").get()
            published_date = each.css("div.meta > div.date::text").get()

            self.logger.debug("爬取文章中...")

            # 封裝
            articleItem = ArticleItem()
            articleItem['article_id'] = article_id
            articleItem['push'] = push
            articleItem['title'] = title
            articleItem['link'] = link
            articleItem['author'] = author           
            articleItem['published_date'] = published_date

            # self.logger.debug(article_id)
            # self.logger.debug(push)
            # self.logger.debug(title)
            # self.logger.debug(link)
            # self.logger.debug(author)
            # self.logger.debug(published_date) 

            yield scrapy.Request(
                url = link,
                callback = self.__parse_each_article,
                cb_kwargs = {'article_id': article_id, 'articleItem':articleItem}
            )
        
    def __parse_each_article(self, response, article_id, articleItem):  # __代表私有變數
        #content
        content = response.css("#main-content::text").getall()
        #設定一個空字串存放content 因為content是list所以要用join加入 並且使用strip來降一些特殊符號去除
        content = "".join(content).strip()

        self.logger.debug("爬取內容中")
        # 封裝
        articleItem['content'] = content
        yield articleItem
        # self.logger.debug(content)

        #comment
        for comment in response.css('.push'): 
            push_tag = comment.css(".push-tag::text").get()
            push_user_id = comment.css(".push-userid::text").get()
            push_content = comment.css(".push-content::text").get()
            push_ipdatetime = comment.css(".push-ipdatetime::text").get()


            self.logger.debug("爬取留言中")
            # 封裝
            commentItem = CommentItem()
            commentItem['article_id'] = article_id
            commentItem['push_tag'] = push_tag
            commentItem['push_user_id'] = push_user_id
            commentItem['push_content'] = push_content
            commentItem['push_ipdatetime'] = push_ipdatetime

            yield commentItem


            # self.logger.debug(article_id)
            # self.logger.debug(push_tag)
            # self.logger.debug(push_user_id)
            # self.logger.debug(push_content)
            # self.logger.debug(push_ipdatetime)