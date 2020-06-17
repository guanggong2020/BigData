# -*- coding: utf-8 -*-
import scrapy
import logging
import copy
from datetime import date
from ..items import FundsItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DailyFundSpider')


class DailyfundsSpider(scrapy.Spider):
    name = 'DailyFunds'
    allowed_domains = [
        'investing.com'
    ]

    def __init__(self):
        self.url = [
            'https://cn.investing.com/funds/usa-funds?&issuer_filter=0'
        ]
        self.y = date.today().year
        self.today = date.today().strftime('%Y-%m-%d')

    def start_requests(self):
        for each in self.url:
            logger.debug(f'现在开始爬取美国每日基金数据------')
            yield scrapy.Request(url=each, callback=self.company_parse)

    def company_parse(self, response):
        content = response.xpath(
            '//select[@class="selectBox float_lang_base_2 js-issuer-filter"]/option/text()'
        ).extract()
        list = []

        try:
            for each in content:
                list.append(each)
        except Exception as e:
            logger.warning(e)

        for _company in list[1:]:
            _url = f'https://cn.investing.com/funds/usa-funds?&issuer_filter={_company}'
            logger.info(f'正爬取 {_company} 的基金数据------')
            yield scrapy.Request(url=_url,
                                 meta={'company': copy.deepcopy(_company), 'download_timeout': 30},
                                 callback=self.funds_parse)

    def funds_parse(self, response):
        _url = 'https://cn.investing.com'
        _company = response.meta['company']

        _rate = response.xpath('//table[@id="etfs"]/tbody/tr/td[5]/text()').extract()
        _date = response.xpath('//table[@id="etfs"]/tbody/tr/td[7]/text()').extract()


        _code = response.xpath('//table[@id="etfs"]/tbody/tr/td[@class="left symbol"]/@title').extract()
        _fund = response.xpath('//table[@id="etfs"]/tbody/tr/td[@class="bold left noWrap elp plusIconTd"]/span/@data-name').extract()
        _href = response.xpath('//table[@id="etfs"]/tbody/tr/td[@class="bold left noWrap elp plusIconTd"]/a/@href').extract()

        for i in range(len(_code)):
            date = _date[i].split('/')
            update_date = f'{self.y}-{date[1]}-{date[0]}'

            if _rate != "0.00%" and update_date <= self.today:
                url = _url + _href[i]

                yield scrapy.Request(url= url,
                                     meta={
                                         'date':copy.deepcopy(update_date),
                                         'code': copy.deepcopy(_code[i]),
                                         'fundName': copy.deepcopy(_fund[i]),
                                         'company': copy.deepcopy(_company),
                                         'download_timeout': 30
                                     },
                                     callback=self.data_parse)

    def data_parse(self, response):
        item = FundsItem()
        _date = response.meta['date']
        item['date'] = response.meta['date']
        item['code'] = response.meta['code']
        item['fundName'] = response.meta['fundName']
        _company = response.meta['company']

        try:

            # if:日期判断

            closingPrice = response.xpath('//span[@id="last_last"]/text()').extract_first()
            change = response.xpath('//div[@class="top bold inlineblock"]/span[2]/text()').extract_first()
            growthRate = response.xpath('//div[@class="top bold inlineblock"]/span[4]/text()').extract_first().replace('%','')

            MorningstarRating = str(len(response.xpath('//*[@id="quotes_summary_secondary_data"]/div/ul/li[1]/span[2]/i[@class="morningStarDark"]').extract()))
            TotalAssets = response.xpath('//*[@id="quotes_summary_secondary_data"]/div/ul/li[2]/span[2]/text()').extract_first()


            OneYearChange = response.xpath('//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[2]/span[2]/text()').extract_first().replace(' ','').replace('%','')
            previousClose = response.xpath('//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[3]/span[2]/text()').extract_first()
            RiskRating = str(len(response.xpath('//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[4]/span[2]/i[@class="morningStarDark"]').extract()))
            TTMYield = response.xpath('//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[5]/span[2]/text()').extract_first().replace('%','')
            ROE = response.xpath('//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[6]/span[2]/text()').extract_first().replace('%','')
            turnover = response.xpath('//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[8]/span[2]/text()').extract_first().replace('%','')
            ROA = response.xpath('//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[9]/span[2]/text()').extract_first().replace('%','')
            totalMarketCapitalization = response.xpath('//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]/div[14]/span[2]/text()').extract_first()


            YTDFundReturn = response.xpath('//table[@class="genTbl openTbl crossRatesTbl"]/tbody/tr[2]/td[2]/text()').extract_first().replace('%','')
            ThreeMonthFundReturn = response.xpath('//table[@class="genTbl openTbl crossRatesTbl"]/tbody/tr[2]/td[3]/text()').extract_first().replace('%','')
            OneYearFundReturn = response.xpath('//table[@class="genTbl openTbl crossRatesTbl"]/tbody/tr[2]/td[4]/text()').extract_first().replace('%','')
            ThreeYearFundReturn = response.xpath('//table[@class="genTbl openTbl crossRatesTbl"]/tbody/tr[2]/td[5]/text()').extract_first().replace('%','')
            FiveYearFundReturn = response.xpath('//table[@class="genTbl openTbl crossRatesTbl"]/tbody/tr[2]/td[6]/text()').extract_first().replace('%','')

            item['closingPrice'] = closingPrice
            item['previousClose'] = previousClose
            item['growthRate'] = growthRate
            item['change'] = change
            item['OneYearChange'] = OneYearChange
            item['turnover'] = turnover
            item['MorningstarRating'] = MorningstarRating
            item['RiskRating'] = RiskRating
            item['TTMYield'] = TTMYield
            item['ROE'] = ROE
            item['ROA'] = ROA
            item['YTDFundReturn'] = YTDFundReturn
            item['ThreeMonthFundReturn'] = ThreeMonthFundReturn
            item['OneYearFundReturn'] = OneYearFundReturn
            item['ThreeYearFundReturn'] = ThreeYearFundReturn
            item['FiveYearFundReturn'] = FiveYearFundReturn
            item['TotalAssets'] = TotalAssets
            item['totalMarketCapitalization'] = totalMarketCapitalization
            item['company'] = _company

            yield item
        except Exception as e:
            logger.warning(e)