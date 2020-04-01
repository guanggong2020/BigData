# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


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


