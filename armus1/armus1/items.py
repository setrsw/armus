# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Armus_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    notify_time = scrapy.Field()
    speaker = scrapy.Field()
    venue = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    college = scrapy.Field()
