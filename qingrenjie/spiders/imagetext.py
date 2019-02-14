# -*- coding: utf-8 -*-
import json

import scrapy
from qingrenjie.items import imageItem


class ImagetextSpider(scrapy.Spider):
    name = 'imagetext'
    allowed_domains = ['capi.douyucdn.cn']
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    offset = 0
    start_urls = [url+str(offset)]

    def parse(self, response):
        data = json.loads(response.text)
        for each in data["data"]:
            item = imageItem()
            item["nickname"] = each["nickname"]
            item["imageurl"] = each["vertical_src"]
            yield item

        if self.offset < 100:
            self.offset += 20
            yield scrapy.Request(url=self.url+str(self.offset), callback=self.parse)
