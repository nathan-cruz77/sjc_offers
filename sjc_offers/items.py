# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Offer(scrapy.Item):
    status = scrapy.Field()
    number = scrapy.Field()
    description = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    max_value = scrapy.Field()
    start_date = scrapy.Field()
