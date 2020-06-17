import scrapy
import logging
from random import randint
import copy
from datetime import datetime
from ..items import FundsItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataSpider')

class DataSpider(scrapy.Spider):
    name = 'fundspider'
    allowed_domains = [
        'investing.com'
    ]

    def __init__(self):
        self.url = [
            'https://cn.investing.com/funds/usa-funds?&issuer_filter=0'
        ]
        self.st_date = '2008/01/01'
        self.end_date = '2020/03/27'

    def start_requests(self):
        for each in self.url:
            logger.debug(f'现在开始爬取美国基金数据------')
            yield scrapy.Request(url=each,callback=self.company_parse)

    def company_parse(self,response):
        content = response.xpath(
            '//select[@class="selectBox float_lang_base_2 js-issuer-filter"]/option/text()'
        ).extract()
        list = []

        try:
            for each in content:
                list.append(each)
        except Exception as e:
            logger.debug(e)

        for _company in list[1:]:
            _url = f'https://cn.investing.com/funds/usa-funds?&issuer_filter={_company}'
            logger.debug(f'正爬取 {_company} 的基金数据------')
            yield scrapy.Request(url=_url,
                                 meta={'company' : copy.deepcopy(_company),'download_timeout': 30},
                                 callback = self.funds_parse)

    def funds_parse(self,response):
        _url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
        _company = response.meta['company']

        _code = response.xpath('//table[@id="etfs"]/tbody/tr/td[@class="left symbol"]/@title').extract()
        _fund = response.xpath('//table[@id="etfs"]/tbody/tr/td[@class="bold left noWrap elp plusIconTd"]/span/@data-name').extract()
        _id = response.xpath('//table[@id="etfs"]/tbody/tr/td[@class="bold left noWrap elp plusIconTd"]/span/@data-id').extract()

        for i in range(len(_code)):
            params = {
                    "curr_id": _id[i],
                    "smlID": str(randint(1000000, 99999999)),
                    "st_date": self.st_date,
                    "end_date": self.end_date,
                    "interval_sec": 'Daily',
                    "sort_col": "date",
                    "sort_ord": "DESC",
                    "action": "historical_data"
                }

            yield scrapy.FormRequest(url=_url,
                                     meta={
                                         'code' : copy.deepcopy(_code[i]),
                                         'fundName' : copy.deepcopy(_fund[i]),
                                         'company' : copy.deepcopy(_company),
                                         'download_timeout': 30,
                                         'params':params
                                     },
                                     formdata=params,
                                     callback=self.data_parse)

    def data_parse(self,response):
        _row = response.xpath('//table[@id="curr_table"]/tbody/tr/td/text()').extract()

        # 六个为一组
        for i in range(0, len(_row), 6):
            each = _row[i:i + 6]

            item = FundsItem()
            # item
            date1 = datetime.strptime(each[0],'%Y年%m月%d日')
            date2 = datetime.strftime(date1,'%Y-%m-%d')
            item['date'] = date2
            item['code'] = response.meta['code']
            item['fundName'] = response.meta['fundName']
            item['closingPrice'] = each[1]
            item['growthRate'] = each[-1].replace('%','')
            item['company'] = response.meta['company']

            yield item