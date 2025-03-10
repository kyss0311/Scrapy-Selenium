import scrapy

class LoginSpider(scrapy.Spider):   # 繼承scrapy.Spider
    name = 'login_demo'
    start_urls = ['https://pythonscraping.com/pages/files/form.html']
    def parse(self, response, **kwargs):
        return scrapy.FormRequest.from_response(
        response,
        # 觀察HTML裡面表單input內的name屬性
        formdata={'firstname': 'Scrapy demo', 'lastname': 'Login'},
        callback=self.after_login
        )
    def after_login(self, response):
        print(response.text)