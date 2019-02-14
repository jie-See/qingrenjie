# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline


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
        image_paths = [x['path'] for ok , x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item