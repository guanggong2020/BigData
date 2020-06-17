# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    positionId = scrapy.Field()
    positionName = scrapy.Field()
    firstType = scrapy.Field()
    secondType = scrapy.Field()
    thirdType = scrapy.Field()
    companyFullName = scrapy.Field()
    companyShortName = scrapy.Field()
    companySize = scrapy.Field()
    industryField = scrapy.Field()
    financeStage = scrapy.Field()
    skillLables = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    positionAdvantage = scrapy.Field()
    jobNature = scrapy.Field()
