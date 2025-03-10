# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import JsonItemExporter  #JSON
from itemadapter import ItemAdapter
from .items import FunnowScraperItem, ProductInfoItem
from . import settings  # relative path import
import psycopg2
import requests


class FunnowScraperPipeline:
    def process_item(self, item, spider):
        if isinstance(item, FunnowScraperItem):
            if item["star"]:
                item["star"] = float(item["star"])
            if item["people"]:
                item['people'] = int(item['people'].strip("()"))
            if item["price"]:
                item['price'] = int(item['price'].replace(",", ""))

        return item

# 輸出json
# class JsonWriterPipeline:
#     # 開啟spider爬蟲時執行 常用於檔案IO的開啟
#     def open_spider(self, spider):
#         self.f = open("funnow-by-JsonItemExporter.json", "wb")  # 必須要是binary mode 寫入bytes
#         self.exporter = JsonItemExporter(self.f, encoding='utf-8')  # 初始化exporter
#         self.exporter.start_exporting()  # 開始匯出
#
#     # 依據傳入的item做處理 務必記得將item回傳
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)  # 匯出資料
#         return item
#
#     # 關閉spider爬蟲時執行 常用於檔案IO的關閉\關閉
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()  # 完成匯出

class DatabasePipeline:

    # 開啟爬蟲時，與postgresql資料庫連線
    def open_spider(self, spider) -> None:

        # 建立connect物件，與postgresql連線
        self.connect = psycopg2.connect(
            host=settings.POSTGRESQL_HOST,
            database=settings.POSTGRESQL_DATABASE,
            user=settings.POSTGRESQL_USERNAME,
            password=settings.POSTGRESQL_PASSWORD
        )
        # 建立cursor物件，以便對資料庫做操作
        self.cursor = self.connect.cursor()
        self.__create_table_if_not_exist()

        # LINE-Notify Token
        self.token = "LscG7tT6NKB9OBJRsXXI7KCXUaOdXjgXfQb8K9vQ2XR"  # 設定 LINE-Notify 權杖

    def lineNotifyMessage(self, msg):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded"  # 設定夾帶內容的型別
        }

        payload = {'message': msg}  # 發送訊息
        res = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)

        if res.status_code != 200:  # 檢查狀態碼
            print('LINE Notify failed')

    def __create_table_if_not_exist(self):
        funnow_sql = """
            CREATE TABLE IF NOT EXISTS funnow( 
                id SERIAL NOT NULL,
                title TEXT, 
                price INT, 
                star FLOAT, 
                people INT, 
                earliest_datetime TEXT, 
                "link" TEXT,
                product_info TEXT,
                product_address TEXT
            );  
        """

        product_sql = """
            CREATE TABLE IF NOT EXISTS "product"( 
                id SERIAL NOT NULL,
                title TEXT, 
                lowest_option_price TEXT, 
                option_info TEXT, 
                option_star TEXT, 
                option_people TEXT, 
                option_datetime TEXT
            );
        """

        self.cursor.execute(funnow_sql)
        self.cursor.execute(product_sql)
        self.connect.commit()

    def process_item(self, item, spider):
        try:
            sql, data = None, None
            if isinstance(item, FunnowScraperItem):
                sql, data = self.__process_funnow_item(item)

            elif isinstance(item, ProductInfoItem):
                sql, data = self.__process_product_item(item)

            if sql is not None and data is not None:
                self.cursor.execute(sql, data)
                self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e)

        return item

    def __process_funnow_item(self, item):
        sql = """
            INSERT INTO funnow(
                title, 
                price,  
                star,  
                people,    
                earliest_datetime, 
                "link",
                product_info,
                product_address
            )VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
            /*ON CONFLICT ON CONSTRAINT funnow_pkey
            DO UPDATE SET push=EXCLUDED.push, title=EXCLUDED.title, content=EXCLUDED.content;*/
        """
        data = (item['title'], item['price'], item['star'], item['people'], item['earliest_datetime'], item['link'],
                item['product_info'], item['product_address'])
        return sql, data

    def __process_product_item(self, item):
        sql = """ 
            INSERT INTO "product"( 
            title, 
            lowest_option_price,  
            option_info,  
            option_star,  
            option_people,
            option_datetime
            )  
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        data = (item["title"], item["lowest_option_price"], item["option_info"],
                item["option_star"], item["option_people"], item["option_datetime"])
        return sql, data

    # 關閉爬蟲時，與postgresql資料庫關閉連線
    def close_spider(self, spider):
        # 找出人數前十多的  ORDER BY：排序 DESC：由多到少 LIMIT 10：限制前十筆
        self.cursor.execute('SELECT title, price, star, product_address, link FROM funnow ORDER BY people DESC LIMIT 10')
        top10 = self.cursor.fetchall()
        # List to tuple [('hello', 15, 'https://...'), ('helloworld', 14, 'https://...'), (), ...]

        # build message
        msg = ''
        for each in top10:
            title, price, star, product_address, link = each
            msg += f"{title} price:{price}, star:{star}, {product_address}\n{link}\n"

        self.lineNotifyMessage(msg)  # 發送訊息

        self.cursor.close()
        self.connect.close()
