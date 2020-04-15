# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import math
import time
import copy
from urllib import parse
import re
import demjson
from ..items import LagouItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataSpider')


class LagouspiderSpider(scrapy.Spider):
    name = 'LagouSpider'
    allowed_domains = ['lagou.com']

    def __init__(self):
        self.url = ['https://www.lagou.com/']
        self.isSchooljob = input('0--社招,1--校招,请输入:')
        # 1--技术,2--产品,3--设计,4--运营,5--市场,6--销售,7--职能,8--游戏
        self.Field = input('1--技术,2--产品,3--设计,4--运营,5--市场,6--销售,7--职能,8--游戏,9--ALL,请输入:')

    def start_requests(self):
        for each in self.url:
            logger.debug('开始爬取拉勾网就业信息----')
            yield scrapy.Request(url=each,meta = {"method":copy.deepcopy("start")},callback=self.main_parse)

    def main_parse(self, response):
        if self.Field == '9':
            tags = response.xpath(
                '//div[@class="mainNavs"]/div/div[@class="menu_sub dn"]/dl/dd/a/h3/text()').extract()
        else:
            tags = response.xpath(
                f'//div[@class="mainNavs"]/div{[self.Field]}/div[@class="menu_sub dn"]/dl/dd/a/h3/text()').extract()

        for each in tags[::-1]:
            URL_tags = parse.quote(each)
            for stage in range(8):
                if self.isSchooljob == '0':
                    _url = f'https://www.lagou.com/jobs/list_{URL_tags}/p-city_0-jd_{stage+1}?px=default'
                else:
                    _url = f'https://www.lagou.com/jobs/list_{URL_tags}/p-city_0-jd_{stage+1}?px=default&isSchoolJob=1'
                for i in range(30)[::-1]:
                    params = {
                        'first': 'false',
                        'pn': i + 1,
                        'kd': each,
                        # 'sid':
                    }
                    yield scrapy.Request(
                        url=_url,
                        meta={
                            "method": copy.deepcopy("page"),
                            "params": copy.deepcopy(params),
                            "referer_URL": copy.deepcopy(_url),
                            "stage": copy.deepcopy(stage),
                            "isSchooljobs": copy.deepcopy(self.isSchooljob)
                        }, callback=self.json_parse
                    )

    def json_parse(self, response):
        item = LagouItem()
        json_data = json.loads(response.body)
        try:
            for each in json_data['content']['positionResult']['result']:
                item['positionId'] = str(each['positionId'])
                item['positionName'] = each['positionName']
                item['firstType'] = each['firstType']
                item['secondType'] = each['secondType']
                item['thirdType'] = each['thirdType']
                item['skillLables'] = each['skillLables']
                item['salary'] = each['salary']
                item['city'] = each['city']
                item['workYear'] = each['workYear']
                item['education'] = each['education']
                item['positionAdvantage'] = each['positionAdvantage']
                item['companyFullName'] = each['companyFullName']
                item['companyShortName'] = each['companyShortName']
                item['companySize'] = each['companySize']
                item['industryField'] = each['industryField'].replace('、', ',')
                item['financeStage'] = each['financeStage']

                yield item

        except Exception as e:
            logger.debug(e)