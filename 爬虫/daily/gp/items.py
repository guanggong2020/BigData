# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataItem(scrapy.Item):
    _id = scrapy.Field()
    date = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    last_price = scrapy.Field()
    highest = scrapy.Field()
    lowest = scrapy.Field()
    begin = scrapy.Field()
    _begin = scrapy.Field()
    diff = scrapy.Field()
    diff_rate = scrapy.Field()
    hand_rate = scrapy.Field()
    deal = scrapy.Field()
    deal_money = scrapy.Field()
    total_value = scrapy.Field()
    _value = scrapy.Field()
