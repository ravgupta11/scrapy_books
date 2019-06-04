# -*- coding: utf-8 -*-
import scrapy


class Spider02Spider(scrapy.Spider):
    name = 'spider02'
    allowed_domains = ['google.com']
    start_urls = ['http://google.com/']

    def parse(self, response):
        pass
