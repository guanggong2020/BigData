import scrapy
import json
import logging
from ..items import DataItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataSpider')

# 日期
# f12:代码 f13:沪/深 f14:名称 f15:最高 f16:最低 f17:今开（开盘价） f18:昨收（前收盘） f20:总市值 f21:流通市值 f23:市净率
# f2:最新价 f3:涨跌幅 f4:涨跌额 f5:成交量 f6:成交额 f8:换手率
# http://26.push2.eastmoney.com/api/qt/clist/get?pn=4&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152
# http://69.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124003746601013421347_1582983102843&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1582983102850
class DataSpider(scrapy.Spider):
    name = 'dataspider'
    allowed_domains = [
        'quotes.money.163.com',
        'quote.eastmoney.com',
        '26.push2.eastmoney.com'
    ]

    def __init__(self):
        self.url = 'http://quote.eastmoney.com/center/gridlist.html#hs_a_board'
        self.num = 0
    def start_requests(self):
        logger.debug(f'现在开始爬取------')
        # meta={'name':i,'download_timeout':30,'page_num':self.page_num},callback=self.parse)
        yield scrapy.Request(url=self.url,callback=self.parse)

    def parse(self,response):
        logger.debug(response.text)
        page_num = response.xpath('//span[@class="paginate_page"]/text()').extract()
        for page in range(196):
            url = f'http://26.push2.eastmoney.com/api/qt/clist/get?pn={str(page+1)}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            yield scrapy.Request(url=url,callback=self.item_parse,meta={'page': str(page+1),'download_timeout': 30})

    def item_parse(self,response):
        item = DataItem()
        page = response.meta['page']
        print(f'正在爬取第{page}页------')
        list = []
        rep = json.loads(response.text)
        try:
            data_list = rep['data']['diff']
            for each in data_list:
                item['code']=each['f12']
                item['name']=each['f14']
                item['last_price']=str(each['f2'])
                item['highest']=str(each['f15'])
                item['lowest']=str(each['f16'])
                item['begin']=str(each['f17'])
                item['_begin']=str(each['f18'])
                item['diff']=str(each['f4'])
                item['diff_rate']=str(each['f3'])
                item['hand_rate']=str(each['f8'])
                item['deal']=str(each['f5'])
                item['deal_money']=str(each['f6'])
                item['total_value']=str(each['f20'])
                item['_value']=str(each['f21'])
                self.num += 1
                yield item
            logger.debug('num = '+ str(self.num))
        except Exception as e:
            logger.debug(e)

