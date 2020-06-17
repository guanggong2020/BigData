# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataItem(scrapy.Item):
    data_type = scrapy.Field()

    _id = scrapy.Field()
    date = scrapy.Field() # 日期
    code = scrapy.Field()  # 股票/基金代码
    name = scrapy.Field()  # 名称
    closingPrice = scrapy.Field()  # 收盘价
    maxPrice = scrapy.Field()  # 最高价
    minPrice = scrapy.Field()  # 最低价
    openingPrice = scrapy.Field()  # 开盘价
    previousClose = scrapy.Field()  # 前收盘
    change = scrapy.Field()  # 涨跌额
    quoteChange = scrapy.Field()  # 涨跌幅
    turnoverRate = scrapy.Field()  # 换手率
    volume = scrapy.Field()  # 成交量
    turnover = scrapy.Field()  # 成交金额
    totalMarketCapitalization = scrapy.Field()  # 总市值
    marketCapitalization = scrapy.Field()  # 流通市值

    fundName = scrapy.Field()  # 基金名称
    unitNetWorth = scrapy.Field()  # 单位净值
    cumulativeNetWorth = scrapy.Field()  # 累计净值
    growthRate = scrapy.Field()  # 增长率

    amplitude = scrapy.Field() # 振幅
    QRR = scrapy.Field() # 量比