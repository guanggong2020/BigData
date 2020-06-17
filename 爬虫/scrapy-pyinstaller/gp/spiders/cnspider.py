import scrapy
import json
import logging
import time
import copy
from random import choice
from datetime import date,timedelta
from selenium import webdriver
from ..items import CnItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataSpider')

# 日期
# f12:代码 f13:沪/深 f14:名称 f15:最高 f16:最低 f17:今开（开盘价） f18:昨收（前收盘） f20:总市值 f21:流通市值 f23:市净率
# f2:最新价 f3:涨跌幅 f4:涨跌额 f5:成交量 f6:成交额 f8:换手率
class DataSpider(scrapy.Spider):
    name = 'dataspider'
    allowed_domains = [
        'quotes.money.163.com',
        'quote.eastmoney.com',
        '26.push2.eastmoney.com',
        'fund.eastmoney.com',
        '27.push2.eastmoney.com'
    ]

    def __init__(self):
        self.flag = int(input('1--A股数据，2--国内基金，3--指数数据，请输入类型：'))
        self.today = date.today()
        self.yesterday = date.today() + timedelta(days=-1)
        self.time = time.strftime("%Y-%m-%d", time.localtime())
        self.url = ['http://quote.eastmoney.com/center/gridlist.html#hs_a_board',
                    f'http://fund.eastmoney.com/data/diyfundranking.html#tall;c0;r;sqjzf;pn50;ddesc;qsd{self.yesterday.strftime("%Y%m%d")};qed{self.today.strftime("%Y%m%d")};qdii']
        self.num = 0
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')  # 增加无界面选项
        # chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
        # chrome_options.add_argument("window-size=1024,768")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument(choice(settings['USER_AGENT_CHOICES']))
        # self.bro = webdriver.Chrome(executable_path=r'/root/spider/A_gp/gp/chromedriver',options=chrome_options)
        # self.bro = webdriver.Chrome(executable_path=r'chromedriver.exe',options=chrome_options)

    def start_requests(self):
        if self.flag == 1:
            logger.info('现在开始爬取股票数据------')
            yield scrapy.Request(url=self.url[0],callback=self.parse)

        elif self.flag == 2:
            logger.info('现在开始爬取基金数据------')
            yield scrapy.Request(url=self.url[1],callback=self.jijin_parse)

        elif self.flag == 3:
            logger.info('现在开始爬取指数数据------')
            # 上证
            for page in range(11):
                url = f'http://27.push2.eastmoney.com/api/qt/clist/get?pn={str(page + 1)}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:1+s:2&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152'
                yield scrapy.Request(url=url, callback=self.item_zhishu_parse,
                                     meta={'type': copy.deepcopy(2), 'download_timeout': 30})

            # 深证
            for page in range(20):
                url = f'http://27.push2.eastmoney.com/api/qt/clist/get?pn={str(page + 1)}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:5&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152'
                yield scrapy.Request(url=url, callback=self.item_zhishu_parse,
                                     meta={'type': copy.deepcopy(3), 'download_timeout': 30})

        else:
            logger.warning('输入错误，结束进程。')
            pass

    def parse(self,response):
        #page_num = response.xpath('//span[@class="paginate_page"]/a/text()')[-1].extract()
        page_num='200'
        # logger.debug('页数:' + page_num)
        #self.bro.quit()
        for page in range(int(page_num)):
            url = f'http://26.push2.eastmoney.com/api/qt/clist/get?pn={str(page+1)}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            yield scrapy.Request(url=url,callback=self.item_parse,meta={'page': str(page+1),'download_timeout': 30})

    def jijin_parse(self,response):
        try:
            #page_num = response.xpath('//div[@id="pagebar"]/label/text()')[-2].extract()
            page_num = '175'
            logger.debug('页数:' + page_num)
            #self.bro.quit()
        except Exception as e:
            logger.warning('Fund Page Connection Error')
            page_num = 175

        for page in range(int(page_num)):
            url = f'http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft=all&rs=&gs=0&sc=qjzf&st=desc&sd={self.yesterday.strftime("%Y-%m-%d")}&ed={self.today.strftime("%Y-%m-%d")}&es=0&qdii=&pi={str(page+1)}&pn=50&dx=0&v=0.5971676275137225'
            yield scrapy.Request(url=url,callback=self.item_jijin_parse,meta={'page': str(page+1),'download_timeout': 30})

    def item_parse(self,response):
        item = CnItem()
        page = response.meta['page']
        rep = json.loads(response.text)
        try:
            data_list = rep['data']['diff']
            for each in data_list:
                item['date']=self.time
                item['data_type']=0 # 股票
                item['code']=each['f12']
                item['name']=each['f14']
                item['closingPrice']=str(each['f2'])
                item['maxPrice']=str(each['f15'])
                item['minPrice']=str(each['f16'])
                item['openingPrice']=str(each['f17'])
                item['previousClose']=str(each['f18'])
                item['change']=str(each['f4'])
                item['quoteChange']=str(each['f3'])
                item['turnoverRate']=str(each['f8'])
                item['volume']=str(each['f5'])
                item['turnover']=str(each['f6'])
                item['totalMarketCapitalization']=str(each['f20'])
                item['marketCapitalization']=str(each['f21'])
                self.num += 1
                yield item
            logger.debug('num = '+ str(self.num))
        except Exception as e:
            logger.warning(e)

    def item_jijin_parse(self,response):
        item = CnItem()
        page = response.meta['page']
        context = response.text.split('[')[1].split(']')[-2].split('\",\"')
        for each in context:
            list = each.strip('\"').split(',')
            item['date']=self.time
            item['data_type'] = 1 # 基金
            item['code'] = list[0]
            item['fundName'] = list[1]
            item['growthRate'] = list[3]
            item['unitNetWorth'] = list[10]
            item['cumulativeNetWorth'] = list[11]
            yield item

    def item_zhishu_parse(self,response):
        item = CnItem()
        type = response.meta['type']
        rep = json.loads(response.text)
        # f12：代码，f14：名称，f2：最新价，f3：涨跌幅，f4：涨跌额，f5：成交量，f6：成交额，f7：振幅，
        # f10：量比，f15：最高，f16：最低，f17：今开，f18：昨收
        try:
            data_list = rep['data']['diff']
            for each in data_list:
                item['date'] = self.time
                item['data_type'] = type # 2:上证 ，3:深证
                item['code'] = each['f12']
                item['name'] = each['f14']
                item['closingPrice'] = str(each['f2'])
                item['maxPrice'] = str(each['f15'])
                item['minPrice'] = str(each['f16'])
                item['openingPrice'] = str(each['f17'])
                item['previousClose'] = str(each['f18'])
                item['change'] = str(each['f4'])
                item['quoteChange'] = str(each['f3'])
                item['volume'] = str(each['f5'])
                item['turnover'] = str(each['f6'])
                item['amplitude'] = str(each['f7'])
                item['QRR'] = str(each['f10'])
                yield copy.deepcopy(item)
        except Exception as e:
            logger.warning(e)