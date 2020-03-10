import scrapy
import json
import logging
import time
from datetime import date,timedelta
from selenium import webdriver
from ..items import DataItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
logging.basicConfig(level=logging.DEBUG)
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
        'fund.eastmoney.com'
    ]

    def __init__(self):
        self.today = date.today()
        self.yesterday = date.today() + timedelta(days=-1)
        self.time = time.strftime("%Y-%m-%d", time.localtime())
        self.url = ['http://quote.eastmoney.com/center/gridlist.html#hs_a_board',
                    f'http://fund.eastmoney.com/data/diyfundranking.html#tall;c0;r;sqjzf;pn50;ddesc;qsd{self.yesterday.strftime("%Y%m%d")};qed{self.today.strftime("%Y%m%d")};qdii'
                    ]
        self.num = 0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # 增加无界面选项
        chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument("--no-sandbox")
        self.bro = webdriver.Chrome(executable_path=r'/root/gp/chromedriver',options=chrome_options)
        # self.bro = webdriver.Chrome(executable_path=r'chromedriver.exe',options=chrome_options)

    def start_requests(self):
        for each in self.url:
            if each in ['http://quote.eastmoney.com/center/gridlist.html#hs_a_board']:
                logger.debug(f'现在开始爬取股票数据------')
                yield scrapy.Request(url=each,callback=self.parse)
            else:
                logger.debug(f'现在开始爬取基金数据------')
                yield scrapy.Request(url=each,callback=self.jijin_parse)

    def parse(self,response):
        page_num = response.xpath('//span[@class="paginate_page"]/a/text()')[-1].extract()
        logger.debug('页数:' + page_num)
        self.bro.quit()
        for page in range(int(page_num)):
            url = f'http://26.push2.eastmoney.com/api/qt/clist/get?pn={str(page+1)}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            yield scrapy.Request(url=url,callback=self.item_parse,meta={'page': str(page+1),'download_timeout': 30})

    def jijin_parse(self,response):
        page_num = response.xpath('//div[@id="pagebar"]/label/text()')[-2].extract()
        logger.debug('页数:' + page_num)
        self.bro.quit()
        for page in range(int(page_num)):
            url = f'http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft=all&rs=&gs=0&sc=qjzf&st=desc&sd={self.yesterday.strftime("%Y-%m-%d")}&ed={self.today.strftime("%Y-%m-%d")}&es=0&qdii=&pi={str(page+1)}&pn=50&dx=0&v=0.5971676275137225'
            yield scrapy.Request(url=url,callback=self.item_jijin_parse,meta={'page': str(page+1),'download_timeout': 30})

    def item_parse(self,response):
        item = DataItem()
        page = response.meta['page']
        print(f'正在爬取股票第{page}页------')
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
            logger.debug(e)

    def item_jijin_parse(self,response):
        item = DataItem()
        page = response.meta['page']
        print(f'正在爬取基金第{page}页------')
        context = response.text.split('[')[1].split(']')[-2].split('\",\"')
        for each in context:
            list = each.strip('\"').split(',')
            # logger.debug(list)
            item['date']=self.time
            item['data_type'] = 1 # 基金
            item['code'] = list[0]
            item['fundName'] = list[1]
            item['growthRate'] = list[3]
            item['unitNetWorth'] = list[10]
            item['cumulativeNetWorth'] = list[11]
            yield item
