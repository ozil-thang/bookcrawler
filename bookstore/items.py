# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookstoreItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    datePublished = scrapy.Field()
    numberOfPages = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()


