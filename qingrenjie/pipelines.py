# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
import pymysql


class QingrenjiePipeline(object):
    def process_item(self, item, spider):
        self.db['problem'].update_one({'title': item['title']}, {'$set': dict(item)}, True)
        return item

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['problems']


class imageTest(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        image_url = item['imageurl']
        yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class mysqltest(object):
    def __init__(self):
        self.db = None
        self.cursor = None

    def process_item(self, item, spider):
        self.db = pymysql.connect(host="localhost", user='root', passwd='shizhijie', db='python3')
        self.cursor = self.db.cursor()

        nickname = item["nickname"]
        imageurl = item['imageurl']

        insert_sql = "INSERT INTO image (nickname, imageurl) VALUES (%s,%s)"
        try:
            self.cursor.execute(insert_sql, (nickname, imageurl))
            self.db.commit()
        except Exception as e:
            print('问题数据跳过.......', e)
            self.db.rollback()
        self.cursor.close()
        self.db.close()
        return item


import xlsxwriter


class excelsave(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook("tencent.xlsx")
        self.worksheet = self.workbook.add_worksheet("first_sheet")
        self.x = 0

    def open_spider(self, spider):
        # spider (Spider 对象) – 被开启的spider
        # 可选实现，当spider被开启时，这个方法被调用。
        pass

    def process_item(self, item, spider):
        self.worksheet.write(self.x, 0, item["title"])
        self.worksheet.write(self.x, 1, item["city"])
        self.worksheet.write(self.x, 2, item["time"])
        self.x += 1
        # self.close_spider(item)
        return item

    def close_spider(self, spider):
        # spider (Spider 对象) – 被关闭的spider
        # 可选实现，当spider被关闭时，这个方法被调用
        self.workbook.close()
