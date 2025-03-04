import scrapy
from scrapy_selenium import SeleniumRequest

from  ..items import KkdayScraperItem

from scrapy.shell import inspect_response

class KkdaySpider(scrapy.Spider):
    name = "kkday"
    allowed_domains = ["www.kkday.com"]
    # start_urls = ["https://www.kkday.com/zh-tw"]

    url = "https://www.kkday.com/zh-tw/destination/tw-new-taipei-city/"
    categories = ['attraction-tickets/list', 'accommodation/list', 'experiences/list/']

    def start_requests(self):
        yield SeleniumRequest(
            url=self.url + self.categories[0],
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        # inspect_response(response, self)
        # self.logger.warning(response.css(".product-listview h3 span::text").get())

        print(f"scraping {self.url+self.categories[0]}...")

        for listview in [response.css('.product-listview')]:
            item = KkdayScraperItem()

            title = listview.css(".product-listview__name").get()
            link = listview.css("a::attr(href)").get()
            tag = [tag.strip() for tag in listview.css(".product-listview__inco_info--flex_item i::text").getall()]
            rate = listview.css(".product-star span::text").get()

            item['title'] = title.strip() if title is not None else title
            item['link'] = link
            item['tag'] = tag
            item['rate'] = rate.strip() if rate is not None else rate

            yield SeleniumRequest(
                url=item['link'],
                wait_time=5,
                callback=self.__parse_each_card,
                cb_kwargs={"item": item}
            )

    def __parse_each_card(self, response, item):
        print(f"scraping {response.url}...")

        product_info = "\n".join([info.strip() for info in response.css("div#prodInfo *::text").getall()])
        item["product_info"] = product_info

        item["option"] = []
        for option in response.css(".option-item"):
            option_content = "".join(option.css(".option-content *::text").getall())
            product_price = option.css(".kk-price-base kk-price-base__origin::text").getall()

            item["option"].append({
                "option_content": option_content.strip() if option_content is not None else option_content,
                "product_price": product_price.strip() if product_price is not None else product_price
            })
        yield item