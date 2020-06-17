# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataItem(scrapy.Item):
    num = scrapy.Field()

    _id = scrapy.Field()
    date = scrapy.Field() # 日期
    code = scrapy.Field()  # 股票/基金代码
    name = scrapy.Field()  # 名称
    latestPrice = scrapy.Field()  # 最新价
    maxPrice = scrapy.Field()  # 最高价
    minPrice = scrapy.Field()  # 最低价
    openingPrice = scrapy.Field()  # 开盘价
    previousClose = scrapy.Field()  # 前收盘
    change = scrapy.Field()  # 涨跌额
    quoteChange = scrapy.Field()  # 涨跌幅(百分数)
    turnoverRate = scrapy.Field()  # 换手率(百分数)
    volume = scrapy.Field()  # 成交量
    turnover = scrapy.Field()  # 成交金额
    totalMarketCapitalization = scrapy.Field()  # 总市值(美元)
    amplitude = scrapy.Field()  # 振幅(百分数)
    PER = scrapy.Field() # 市盈率(百分数)
    QRR = scrapy.Field() # 量比
    PBR = scrapy.Field() # 市净率(百分数)
    TTM = scrapy.Field() # 上市时间
    EPS = scrapy.Field() # 每股收益
    NAVPS = scrapy.Field() # 每股净资产



