import aiohttp
import asyncio
from random import choice
import time
import os
import csv
from tqdm import tqdm



class ZS_Spider(object):
    def __init__(self,SEM,SH,SZ,ZS_PATH,ZS_DATA,START_TIME,END_TIME):
        self.USER_AGENT = [
                'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
                'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
                'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
                'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
                'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
                'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)',
            ]
        # self.IN_con = pymongo.MongoClient('mongodb://134.175.192.53:27017')
        # self.IN_con.admin.authenticate('admin','@Admin123')
        self.mycol = ZS_DATA
        self.SH = SH
        self.SZ = SZ
        self.sem = asyncio.Semaphore(SEM) #信号量，控制协程数
        self.filepath = ZS_PATH
        self.START_TIME = START_TIME
        self.END_TIME = END_TIME

    async def get_content(self,link):
        async with self.sem:
            async with aiohttp.ClientSession() as session:# cookie字典在clientsession中自定义
                async with session.get(link,headers = {'User-Agent':choice(self.USER_AGENT)},timeout = 30) as rep:
                    content = await rep.read()
                    return content

    def get_url(self,num,type):
        start_time = self.START_TIME
        end_time = self.END_TIME
        # 深证
        if type == 0:
            url = f'http://quotes.money.163.com/service/chddata.html?code=1{num}&start={start_time}&end={end_time}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'
            yield url
        # 上证
        else:
            url = f'http://quotes.money.163.com/service/chddata.html?code=0{num}&start={start_time}&end={end_time}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'
            yield url

    async def download_csv(self,link,num):
        condition = {'code': num}
        file_name = self.filepath + num + '.csv'
        try:
            content = await self.get_content(link)
            with open(file_name, 'wb') as f:
                f.write(content)
            print('下载成功 {}'.format(file_name))
        except Exception as e:
            print('下载失败 {}'.format(file_name))

    def run(self):
        # 下载csv文件
        start = time.time()

        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)

        # 上证
        for num in self.SZ.find():
            #if num['status'] == 0:
            num = num['code']
            type = 0
            tasks = [asyncio.ensure_future(self.download_csv(link,num)) for link in self.get_url(num,type)]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))

        for num in self.SH.find():
            num = num['code']
            type = 1
            tasks = [asyncio.ensure_future(self.download_csv(link, num)) for link in self.get_url(num, type)]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
        end = time.time()
        print('csv下载共运行了{}秒'.format(end-start))

        self.csv_to_mongo()

    def csv_to_mongo(self):
        start = time.time()
        count = 0
        fileList = os.listdir(self.filepath)
        # 依次对每个数据文件进行存储
        for fileName in tqdm(fileList):
            list = []
            with open(self.filepath + fileName,'r',encoding='gbk') as csvfile:
                data = csv.DictReader(csvfile)
                try:
                    for each in data:
                        dic = {
                            'date':each['日期'].replace('/','-').strip(),
                            'code':each['股票代码'].replace('\'','').strip(),
                            'name':each['名称'].strip(),
                            'closingPrice':each['收盘价'].strip(),
                            'maxPrice':each['最高价'].strip(),
                            'minPrice':each['最低价'].strip(),
                            'openingPrice':each['开盘价'].strip(),
                            'previousClose':each['前收盘'].strip(),
                            'change':each['涨跌额'].strip(),
                            'quoteChange':each['涨跌幅'].strip(),
                            'volume':each['成交量'].strip(),
                            'turnover':each['成交金额'].strip()
                        }
                        list.append(dic)
                        count += 1
                    self.mycol.insert_many(list)
                except Exception as e:
                    print(e)

        end = time.time()
        print('成功插入了{}条数据'.format(str(count)))
        print('存储到mongodb共运行了{}秒'.format(end-start))

    
