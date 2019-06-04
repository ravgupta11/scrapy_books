# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os

from scrapy import Request
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline


class BooksToScrapePipeline1(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'tag': item['tag'], 'title': item['title']}) for x in
                item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block
        tag = request.meta['tag']
        title = request.meta['title']
        return '%s/%s.jpg' % (tag, title)


class BooksToScrapePipeline2(object):
    def open_spider(self, spider):
        self.tag_to_exporter = {}
        print("############################################################" * 3 + spider.output)

    def close_spider(self, spider):
        for exporter in self.tag_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item, spider):
        tag = item['tag']
        title = item['title']
        if (tag, title) not in self.tag_to_exporter:
            PATH = 'FILES\\' + tag
            if not os.path.exists(PATH):
                os.makedirs(PATH)
            if (spider.output == 'json'):
                f = open('%s\%s.json' % (PATH, title), 'wb')
                exporter = JsonItemExporter(f)
            else:
                f = open('%s\%s.csv' % (PATH, title), 'wb')
                exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.tag_to_exporter[(tag, title)] = exporter
        return self.tag_to_exporter[(tag, title)]

    def process_item(self, item, spider):
        item['price'] = item['price'][0]
        item['rating'] = item['rating'][0]
        item['tag'] = item['tag'][0]
        item['title'] = item['title'][0]
        item['product_desc'] = item['product_desc'][0]
        exporter = self._exporter_for_item(item, spider)
        exporter.export_item(item)
        return item
