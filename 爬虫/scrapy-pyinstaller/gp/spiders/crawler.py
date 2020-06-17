import scrapy
import json
import logging
import time
from selenium import webdriver
from ..items import StockItem
# 传递item时出错，发现是使用Request函数传递item时，使用的是浅复制，需要用copy包的deepcopy
import copy
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataSpider')

class StockSpider(scrapy.Spider):
    name = 'stockspider'
    allowed_domains = [
        'quote.eastmoney.com',
        '26.push2.eastmoney.com',
        '71.push2.eastmoney.com',
        'push2.eastmoney.com'
    ]

    def __init__(self):
        # 时间定义
        self.time = time.strftime("%Y-%m-%d", time.localtime())

        self.url = ['http://quote.eastmoney.com/center/gridlist.html#us_stocks']
        self.num = 0

        # selenium
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')  # 增加无界面选项
        # chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
        # chrome_options.add_argument("window-size=1024,768")
        # chrome_options.add_argument("--no-sandbox")
        # self.bro = webdriver.Chrome(executable_path=r'/root/spider/A_gp/gp/chromedriver',options=chrome_options)
        # self.bro = webdriver.Chrome(executable_path=r'chromedriver.exe',options=chrome_options)

    def start_requests(self):
        for each in self.url:
            logger.info(f'现在开始爬取美股代码------')
            yield scrapy.Request(url=each,callback=self.parse)

    def parse(self,response):
        # page_num = response.xpath('//span[@class="paginate_page"]/a/text()')[-1].extract()
        page_num = '451'
        #logger.debug('页数:' + page_num)
        # self.bro.quit()
        for page in range(int(page_num)):
            url = f'http://71.push2.eastmoney.com/api/qt/clist/get?pn={page}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:105,m:106,m:107&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152&_=1583929895110'
            yield scrapy.Request(url=url,callback=self.page_parse,meta={'page': str(page+1),'download_timeout': 30})

    def page_parse(self,response):
        item = StockItem()
        page = response.meta['page']
        rep = json.loads(response.text)
        try:
            data_list = rep['data']['diff']
            for each in data_list:
                # 日期
                item['date'] = self.time
                # f12:代码，注意将代码中的.替换成_
                item['code'] = each['f12']
                # f14:名称
                item['name'] = each['f14']
                # f2:最新价(美元)
                item['latestPrice'] = str(each['f2'])
                # f17:今开
                item['openingPrice'] = str(each['f17'])
                # f18:昨收
                item['previousClose'] = str(each['f18'])
                # f15:最高价
                item['maxPrice'] = str(each['f15'])
                # f16:最低价
                item['minPrice'] = str(each['f16'])
                # f3:涨跌幅(百分数)，根据该参数判断secid参数
                item['quoteChange'] = str(each['f3'])
                # f4:涨跌额
                item['change'] = str(each['f4'])
                # f5:成交量
                item['volume'] = str(each['f5'])
                # f6:成交额
                item['turnover'] = str(each['f6'])
                # f7:振幅(百分数)
                item['amplitude'] = str(each['f7'])
                # f8:换手率(百分数)
                item['turnoverRate'] = str(each['f8'])
                # f9:市盈率(百分数)
                item['PER'] = str(each['f9'])
                # f10:量比
                item['QRR'] = str(each['f10'])
                # f23:市净率
                item['PBR'] = str(each['f23'])
                # f20:总市值（美元）
                item['totalMarketCapitalization'] = str(each['f20'])
                # f26:上市时间
                item['TTM'] = str(each['f26'])
                # 迭代次数
                item['num'] = 0
                code = each['f12'].replace('.','_')
                # yield item
                yield scrapy.Request(
                    url=f'http://push2.eastmoney.com/api/qt/stock/get?secid=105.{code}&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f55,f92&type=CT&cmd=VIIX7&sty=FDPBPFB&st=z&js=((x))&token=4f1862fc3b5e77c150a2b985b12db0fd&_=1583983672971',
                    callback=self.next_parse, meta = {'item':copy.deepcopy(item),'download_timeout': 30}
                                     )
            # self.num += 1
        except Exception as e:
            logger.warning(e)

    def next_parse(self,response):
        item = response.meta['item']
        rep = json.loads(response.text)
        if item['num'] == 0:
            try:
                # next:f55-每股收益 ，f92-每股净资产
                item['EPS'] = str(rep['data']['f55'])
                item['NAVPS'] = str(rep['data']['f92'])
                yield copy.deepcopy(item)
            except Exception as e:
                logger.warning(e)
                item['num'] += 1
                code = item['code'].replace('.','_')
                yield scrapy.Request(
                        url=f'http://push2.eastmoney.com/api/qt/stock/get?secid=106.{code}&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f55,f92&type=CT&cmd=VIIX7&sty=FDPBPFB&st=z&js=((x))&token=4f1862fc3b5e77c150a2b985b12db0fd&_=1583983672971',
                        callback=self.next_parse, meta = {'item':copy.deepcopy(item),'download_timeout': 30}
                                         )
        elif item['num'] == 1:
            try:
                item['EPS'] = str(rep['data']['f55'])
                item['NAVPS'] = str(rep['data']['f92'])
                yield copy.deepcopy(item)
            except Exception as e:
                logger.warning(e)
                item['num'] += 1
                code = item['code'].replace('.', '_')
                yield scrapy.Request(
                        url=f'http://push2.eastmoney.com/api/qt/stock/get?secid=107.{code}&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f55,f92&type=CT&cmd=VIIX7&sty=FDPBPFB&st=z&js=((x))&token=4f1862fc3b5e77c150a2b985b12db0fd&_=1583983672971',
                        callback=self.next_parse, meta = {'item':copy.deepcopy(item),'download_timeout': 30}
                                         )
        else:
            try:
                item['EPS'] = str(rep['data']['f55'])
                item['NAVPS'] = str(rep['data']['f92'])
                yield copy.deepcopy(item)
            except Exception as e:
                logger.warning(e)
                item['EPS'] = 0.0
                item['NAVPS'] = 0.0
                yield copy.deepcopy(item)