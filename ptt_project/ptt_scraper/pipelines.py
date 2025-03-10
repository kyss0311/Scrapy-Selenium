# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import JsonItemExporter  #JSON
from itemadapter import ItemAdapter
from .items import ArticleItem, CommentItem
from . import settings  # relative path import 
import psycopg2
import requests

# 更改格式
class PttScraperPipeline:
# 依據傳入的item做處理 務必記得將item回傳
    def process_item(self, item, spider):
        
        # 進階
        #  把push的字串轉成整數(int)儲存
        # 1. 空的就是0
        # 2. 遇到"爆"就是超過百推，以100計
        # 3. 遇到X開頭代表"噓留言"大於"推留言"，X1代表噓比推多10，
        # X2代表噓比推多20，XX代表噓比推多100以上
                
        if isinstance(item, ArticleItem):
            # empty push
            if item["push"] is None:
                item['push'] = 0

            # '爆'
            elif item["push"] == '爆':
                item['push'] = 100

            # 'X'
            elif 'X' in item['push']:
                boo_cnt = item['push'].split('X')[-1]
                #'X'
                if boo_cnt == '':
                    item['push'] = -10
                #'XX'
                elif boo_cnt == 'X':
                    item['push'] = -100
                # 'X2' 'X3' ...
                else:
                    item['push'] = -int(boo_cnt)*10
            # '12' , '65' ...
            else:
                item['push'] = int(item['push'])

        return item


# 輸出json
class JsonWriterPipeline:
    # 開啟spider爬蟲時執行 常用於檔案IO的開啟
    def open_spider(self, spider):
        self.f = open("ptt-by-JsonItemExporter.json", "wb")   # 必須要是binary mode 寫入bytes 
        self.exporter = JsonItemExporter(self.f, encoding = 'utf-8')  # 初始化exporter
        self.exporter.start_exporting()   # 開始匯出


    # 依據傳入的item做處理 務必記得將item回傳
    def process_item(self, item, spider):
        self.exporter.export_item(item)  # 匯出資料
        return item
    
    
    # 關閉spider爬蟲時執行 常用於檔案IO的關閉\關閉
    def close_spider(self, spider):
        self.exporter.finish_exporting()  # 完成匯出

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

        article_sql = """
            CREATE TABLE IF NOT EXISTS article( 
                id SERIAL NOT NULL, 
                article_id TEXT PRIMARY KEY, 
                push INT, 
                title TEXT, 
                "link" TEXT, 
                author TEXT, 
                published_date TEXT, /*ex: 5/26*/ 
                "content" TEXT  
            );  
        """

        commemt_sql = """
            CREATE TABLE IF NOT EXISTS "comment"( 
                id SERIAL NOT NULL, 
                article_id TEXT, 
                push_tag TEXT, 
                push_user_id TEXT, 
                push_content TEXT, 
                push_ipdatetime TEXT, /*ex: 05/26 08:57*/ 
                FOREIGN KEY(article_id) REFERENCES article(article_id) ON DELETE CASCADE 
                /*當兩表都有該筆資料，一起刪掉*/ 
            );
        """

        self.cursor.execute(article_sql)
        self.cursor.execute(commemt_sql)
        self.connect.commit()

    def process_item(self, item, spider):
        try:
            sql, data = None, None
            if isinstance(item, ArticleItem):
                sql, data = self.__process_article_item(item)
                delete_sql = 'DELETE FROM "comment" WHERE article_id = %s'
                delete_data = (item["article_id"],)  # 小心! 必須是tuple 後面加逗號可以設定成tuple
                self.cursor.execute(delete_sql, delete_data)

            elif isinstance(item, CommentItem):
                sql, data = self.__process_comment_item(item)

            if sql is not None and data is not None:
                self.cursor.execute(sql, data)
                self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e)

        return item

    def __process_article_item(self, item):
        sql = """
            INSERT INTO article(
                article_id, 
                push,  
                title,  
                "link",  
                author,  
                published_date, 
                "content"
            )VALUES(%s, %s, %s, %s, %s, %s, %s);
            ON CONFLICT ON CONSTRAINT article_pkey
            DO UPDATE SET push=EXCLUDED.push, title=EXCLUDED.title, content=EXCLUDED.content;
        """
        data = (item['article_id'], item['push'], item['title'], item['link'], item['author'], item['published_date'], item['content'])
        return sql, data
    
    def __process_comment_item(self, item):
        sql = """ 
            INSERT INTO "comment"( 
            article_id, 
            push_tag,  
            push_user_id,  
            push_content,  
            push_ipdatetime 
            )  
            VALUES (%s, %s, %s, %s, %s);
        """ 
        data = (item["article_id"], item["push_tag"], item["push_user_id"], item["push_content"], item["push_ipdatetime"])
        return sql, data

    # 關閉爬蟲時，與postgresql資料庫關閉連線 
    def close_spider(self, spider):
        # 找出貼文推前十多的 ORDER BY：排序 DESC：由多到少 LIMIT 10：限制前十筆
        self.cursor.execute('SELECT title, push, link FROM article ORDER BY push DESC LIMIT 10')
        top10 = self.cursor.fetchall()
        # List to tuple [('hello', 15, 'https://...'), ('helloworld', 14, 'https://...'), (), ...]

        # build message
        msg = ''
        for each in top10:
            title, push, link = each
            # title = each[0]
            # push = each[1]
            # link = each[2]

            msg += f"{push} {title} {link}\n"

        # self.lineNotifyMessage(msg)  # 發送訊息

        self.cursor.close() 
        self.connect.close()

