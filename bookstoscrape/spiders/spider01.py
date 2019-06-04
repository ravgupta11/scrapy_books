# -*- coding: utf-8 -*-
import scrapy
from bookstoscrape.items import BookstoscrapeItem
from scrapy.loader import ItemLoader


class Spider01Spider(scrapy.Spider):
    name = 'spider01'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def __init__(self, output='', *args, **kwargs):
        self.output = output
        super(Spider01Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        books = response.xpath('//ol[@class="row"]/li')
        for book in books:
            relative_url = book.xpath('.//a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            yield scrapy.Request(url=absolute_url, callback=self.parse_book)
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_url_next = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_url_next)

    def parse_book(self, response):
        I = ItemLoader(item=BookstoscrapeItem(), response=response)
        I.add_value('tag', response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').extract_first())
        I.add_value('title', response.xpath('//h1/text()').extract_first())
        I.add_value('price', response.xpath('//p[@class="price_color"]/text()').extract_first())
        I.add_value('rating', response.xpath('//p[contains(@class, "star-rating")]/@class').extract_first().replace(
            "star-rating ", ""))
        iurl = response.xpath('//img/@src').extract_first().replace("../..", "http://books.toscrape.com")
        I.add_value('image_urls', iurl)
        I.add_value('product_desc',
                    response.xpath('//div[@id="product_description"]/following-sibling::*/text()').extract_first())
        return I.load_item()
