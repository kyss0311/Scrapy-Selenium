# from typing import Iterable

import scrapy
# from scrapy import Request
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException


class YoutubeSeleniumTestSpider(scrapy.Spider):
    name = "youtube_selenium_test"
    allowed_domains = ["www.youtube.com"]
    # start_urls = ["https://www.youtube.com/watch?v=eZh1mC1vPgw"]

    start_url = "https://www.youtube.com/watch?v=eZh1mC1vPgw"

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_url,
            callback=self.parse,
            wait_time=10,  # timeout(過期)的時間，程式會等待wait_until的條件滿足，直到超過timeout時間
            wait_until=EC.visibility_of_element_located((By.CSS_SELECTOR, "#below")),
            script="window.scroll(0, 500)"  # 執行javascript語言，讓卷軸往下滾動500px，水平方向則不動
        )

    def parse(self, response, **kwargs):

        try:
            driver = response.request.meta['driver']  # 取得selenium當前的driver實例物件
            expandBtn = WebDriverWait(driver, timeout=50)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#expand")))  # 使用WebDriverWait等待
            expandBtn.click()

            result = ""
            description = response.css("#description *::text").getall()
            for text in description:
                if text.strip() != "":
                    result = result + text.strip() + "\n"
            print(result)
        except TimeoutException:
            print("Reach timeout")git
        except NoSuchElementException as e:
            print(e.msg)
        except ElementNotInteractableException as e:
            print(e.msg)
            print(expandBtn.get_attribute("id"))  # 用selenium取得當前元素的id
