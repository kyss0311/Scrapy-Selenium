# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import psycopg2
from . import settings


class StockScraperPipeline: 
    def process_item(self, item, spider):
        if spider.name == 'stock':
            # 資料日期: 06/20 -> 2022-06-20
            if item['date'] != None and "資料日期: " in item['date']:
                date = item['date'].split('資料日期: ')[-1]  #06/20
                year = str(datetime.now().year)
                item['date'] = datetime.strptime(year+"/"+date, "%Y/%m/%d").strftime("%Y-%m-%d")  #2022-06-20

            item['deal_price'] = float(item['deal_price']) if item['deal_price'] is not None else None
            item['opening_price'] = float(item['opening_price']) if item['opening_price'] is not None else None
            item['closing_price'] = float(item['closing_price']) if item['closing_price'] is not None else None
            item['highest_price'] = float(item['highest_price']) if item['highest_price'] is not None else None
            item['lowest_price'] = float(item['lowest_price']) if item['lowest_price'] is not None else None

        elif spider.name == 'stock-dividend':
            item['rank'] = int(item['rank']) if item['rank'] is not None else None
            item['dividend_distribution_year'] = int(item['dividend_distribution_year']) if item['dividend_distribution_year'] is not None else None
            item['trading_price'] = float(item['trading_price']) if item['trading_price'] is not None else None
            item['cash_dividend'] = float(item['cash_dividend']) if item['cash_dividend'] is not None else None
            item['stock_dividend'] = float(item['stock_dividend']) if item['stock_dividend'] is not None else None
            item['clean_price'] = float(item['clean_price']) if item['clean_price'] is not None else None
            item['cash_yield'] = float(item['cash_yield']) if item['cash_yield'] is not None else None
            item['stock_yield'] = float(item['stock_yield']) if item['stock_yield'] is not None else None
            # 資料日期: 22'/06/20 -> 2022-06-20
            if item['cash_dividend_distribution_date'] is not None:
                item['cash_dividend_distribution_date'] = datetime.strptime(item['cash_dividend_distribution_date'], "'%y/%m/%d").strftime("%Y-%m-%d")

        return item


class DatabasePipeline:

    # 開啟爬蟲時，與postgresql資料庫連線 
    def open_spider(self, spider): 
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
    
    def __create_table_if_not_exist(self):

        stock_price_sql = """
            CREATE TABLE IF NOT EXISTS stock_price( 
                stock_name TEXT,
                date DATE, /* YYYY-MM-DD */
                deal_price FLOAT,
                opening_price FLOAT,
                closing_price FLOAT,
                highest_price FLOAT,
                lowest_price FLOAT
            );  
        """

        stock_dividend_sql = """
            CREATE TABLE IF NOT EXISTS stock_dividend( 
                rank INT,
                code TEXT,
                name TEXT,
                trading_price FLOAT,
                dividend_distribution_year INT,
                cash_dividend FLOAT,
                stock_dividend FLOAT,
                clean_price FLOAT,
                cash_yield FLOAT,
                stock_yield FLOAT,
                cash_dividend_distribution_date DATE
            );
        """

        self.cursor.execute(stock_price_sql)
        self.cursor.execute(stock_dividend_sql)
        self.connect.commit()

    def process_item(self, item, spider):
        try:
            sql, data = None, None
            if spider.name == 'stock':
                sql, data = self.__process_stock_price_item(item)
            elif spider.name == 'stock-dividend':
                sql, data = self.__process_stock_dividend_item(item)

            if sql is not None and data is not None:
                self.cursor.execute(sql, data)
                self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e)

        return item

    def __process_stock_price_item(self, item):
        sql = """
            INSERT INTO stock_price(
                stock_name,
                date,
                deal_price,
                opening_price,
                closing_price,
                highest_price,
                lowest_price
            )VALUES(%s, %s, %s, %s, %s, %s, %s);
        """
        data = (item['stock_name'], item['date'], item['deal_price'], item['opening_price'], item['closing_price'], item['highest_price'], item['lowest_price'])
        return sql, data
    
    def __process_stock_dividend_item(self, item):
        sql = """ 
            INSERT INTO stock_dividend( 
            rank,
            code,
            name,
            trading_price,
            dividend_distribution_year,
            cash_dividend,
            stock_dividend,
            clean_price,
            cash_yield,
            stock_yield,
            cash_dividend_distribution_date 
            )  
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """ 
        data = (item["rank"], item["code"], item["name"], item["trading_price"], item["dividend_distribution_year"],
                item["cash_dividend"], item["stock_dividend"], item["clean_price"], item["cash_yield"], item["stock_yield"], item["cash_dividend_distribution_date"])
        return sql, data

    # 關閉爬蟲時，與postgresql資料庫關閉連線 
    def close_spider(self, spider): 
        self.cursor.close()
        self.connect.close()