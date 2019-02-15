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
