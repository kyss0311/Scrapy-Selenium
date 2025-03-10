# (venv) PS C:\Users\kytu3\Desktop\scrapy_demo\funnow_project>
# scrapy crawl funnow -L WARNING --logfile logging.txt -o funnow.json

import scrapy
from scrapy_selenium import SeleniumRequest
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException,TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ..items import FunnowScraperItem, ProductInfoItem
import time
# 測試模組
# from scrapy.shell import inspect_response

class FunnowSpider(scrapy.Spider):
    name = "funnow"
    allowed_domains = ["www.myfunnow.com"]

    start_urls = "https://www.myfunnow.com"
    url = "https://www.myfunnow.com/zh-tw/regions/1/categories/"
    categories = ['1', '2', '8', '11099']  # 1=休息 2=住宿 8=餐廳酒吧 11099=露營

    def start_requests(self):
        for i in range(len(self.categories)):
            yield SeleniumRequest(
                url=self.url + self.categories[i],  # 初始request是向第一個category發請求
                # selenium會等最多10秒直到出現footer後再擷取當前的頁面HTML
                wait_time=10,
                wait_until=EC.visibility_of_element_located((By.CSS_SELECTOR, "footer")),
                script="window.scroll(0, document.body.scrollHeight)",
                callback=self.parse  # 取得response後要執行的回呼函式
            )
            time.sleep(3)

    def parse(self, response, **kwargs):
        # 測試模組
        # inspect_response(response, self)
        # self.logger.warning(response.css(".product-list .product-info .card-title p::text").get())

        for product in response.css(".product-list__col"):
            item = FunnowScraperItem()

            title = product.css(".product-info .card-title p::text").get()
            price = product.css(".product-info .card-title p span::text").get()
            star = product.css(".product-info div:nth-child(2) div span:nth-child(2)::text").get()
            people = product.css(".product-info div:nth-child(2) div span:nth-child(3)::text").get()
            earliest_datetime = product.css(".product-info div:nth-child(2) span div span::text").get()
            link = product.css("a::attr(href)").get()

            item["title"] = title
            item["price"] = price
            item["star"] = star
            item["people"] = people.strip() if people is not None else people
            item["earliest_datetime"] = earliest_datetime
            item["link"] = link
            if item["link"]:
                item["link"] = "https://www.myfunnow.com" + link

                yield SeleniumRequest(
                    url=item["link"],
                    wait_time=10,
                    callback=self.__parse_each_product,
                    cb_kwargs={"item": item}
                )

    def __parse_each_product(self, response, item):

        info_item = ProductInfoItem()
        product_info = "\n".join([info.strip()
                                  for info in response.css("#main-branch-address .info-content ul *::text").getall()])
        product_address = response.css("#main-branch-address .info-content .branch-address::text").get()

        item["product_info"] = product_info
        item["product_address"] = product_address

        yield item

        for option in response.css("#main-branch-products .wd-w-full"):
            option_name = option.css(".product-info .card-title p::text").get()
            if option_name == None:
                continue
            lowest_option_price = option.css(".product-info .card-title p span::text").get()
            option_info = option.css(".product-info .product-name::text").get()
            option_star = option.css(".product-info div:nth-child(3) div span::text").get()
            option_people = option.css(".product-info div:nth-child(3) div span:nth-last-child(1)::text").get()
            option_datetime = option.css(".product-info div:nth-child(3) span span::text").get()

            info_item["title"] = option_name.strip() if option_name is not None else option_name
            info_item["lowest_option_price"] = lowest_option_price.strip()\
                if lowest_option_price is not None else lowest_option_price
            info_item["option_info"] = option_info
            info_item["option_star"] = option_star
            info_item["option_people"] = option_people
            info_item["option_datetime"] = option_datetime

        yield info_item
