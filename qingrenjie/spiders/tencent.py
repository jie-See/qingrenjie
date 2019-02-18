# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qingrenjie.items import imageItem


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()

        data = response.xpath('//tr[@class="even"] | tr[@class="odd"]')
        for each in data:
            item = imageItem()
            item['title'] = each.xpath('./td[1]/a/text()').extract()[0]
            item['city'] = each.xpath('./td[4]/text()').extract()[0]
            item['time'] = each.xpath('./td[5]/text()').extract()[0]
            yield item
