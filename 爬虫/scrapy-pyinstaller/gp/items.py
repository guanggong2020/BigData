# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CnItem(scrapy.Item):
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

class StockItem(scrapy.Item):
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

class FundsItem(scrapy.Item):
    date = scrapy.Field() #日期
    code = scrapy.Field() #代码
    fundName = scrapy.Field() #基金名称
    closingPrice = scrapy.Field() #收盘价
    previousClose = scrapy.Field() #前收盘
    growthRate = scrapy.Field() #增长率(百分数)
    change = scrapy.Field() #涨跌额
    OneYearChange = scrapy.Field() #一年涨跌幅
    turnover = scrapy.Field() #周转率
    MorningstarRating = scrapy.Field() #晨星评级
    RiskRating = scrapy.Field() #风险评级
    TTMYield = scrapy.Field() #过去十二个月收益率
    ROE = scrapy.Field() #ROE
    ROA = scrapy.Field() #ROA
    YTDFundReturn = scrapy.Field() #年初至今基金回报
    ThreeMonthFundReturn = scrapy.Field() #三个月基金回报
    OneYearFundReturn = scrapy.Field() #一年基金回报
    ThreeYearFundReturn = scrapy.Field() #三年基金回报
    FiveYearFundReturn = scrapy.Field() #五年基金回报
    TotalAssets = scrapy.Field() #总资产
    totalMarketCapitalization = scrapy.Field() #市值
    company = scrapy.Field() #发行商

