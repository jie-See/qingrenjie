# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import FormRequest
from qingrenjie.items import QingrenjieItem


class QinrenSpider(scrapy.Spider):
    name = 'qinren'
    allowed_domains = ['xcx1.sangcr.com']
    start_urls = ['http://xcx1.sangcr.com/']
    headers = {
        ""
    }
    formdata = {
        'category_id': '758',
        'topic_limit': '1000',
        'session_key': 'zxdt_n9uqrktf4cepdkeezwnzhuayh6qhmp9w'
    }

    def start_requests(self):
        url = "https://xcx1.sangcr.com/api/app/getQuestion"
        requests = []
        request = FormRequest(url, callback=self.parse, formdata=self.formdata)
        requests.append(request)
        return requests

    def parse(self, response):

        response = json.loads(response.text)["topics"]
        for a in response:
            item = QingrenjieItem()
            item["title"] = a['title']
            # answer = []
            b = a['list']
            num = len(b)
            if 0 < num:
                item['A'] = b[0]['title']
            if 1 < num:
                item['B'] = b[1]['title']
            if 2 < num:
                item['C'] = b[2]['title']
            if 3 < num:
                item['D'] = b[3]['title']
                # answer.append(b['title'])
            # item["answer"] = answer
            yield item
