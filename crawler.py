import aiohttp
import asyncio
from random import choice
import time
import pymongo
import os
import csv
from tqdm import tqdm
import price_code
import csv_size
# CODES = ['600025','600026','600000','600004','600006','600007']


class Spider(object):
    def __init__(self):
        self.USER_AGENT = [
                'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
                'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
                'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
                'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
                'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
                'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)',
            ]
        self.con = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.con['keshe']
        self.mycol = self.db['test']
        self.sem = asyncio.Semaphore(32) #信号量，控制协程数
        self.filepath = '.\\csv_data\\'
        self.CODES = self.mycol.find()

    async def get_content(self,link):
        async with self.sem:
            async with aiohttp.ClientSession() as session:# cookie字典在clientsession中自定义
                async with session.get(link,headers = {'User-Agent':choice(self.USER_AGENT)},timeout = 30) as rep:
                    content = await rep.read()
                    return content

    def get_url(self,num,start_time='20080101',end_time='20200214'):
        # 深圳股票
        if num.startswith('0') or num.startswith('1') or num.startswith('2') or num.startswith('3'):
            url = f'http://quotes.money.163.com/service/chddata.html?code=1{num}&start={start_time}&end={end_time}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
            yield url
        # 上海股市
        else:
            url = f'http://quotes.money.163.com/service/chddata.html?code=0{num}&start={start_time}&end={end_time}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
            yield url

    async def download_csv(self,link,num):
        condition = {'code': num}
        file_name = self.filepath + num + '.csv'
        try:
            content = await self.get_content(link)
            with open(file_name, 'wb') as f:
                f.write(content)
            print('下载成功 {}'.format(file_name))
            # self.mycol.update_one(condition,{'$set':{'status':1}})
        except Exception as e:
            print('下载失败 {}'.format(file_name))
            # mycol.update_one(condition, {'$set': {'success': 0}})

    def run(self,get_code,get_code_url):
        # 获取股票代码
        if get_code == 1:
            price_code.main(url=get_code_url)
        # 下载csv文件
        start = time.time()
        for num in self.CODES:
            #if num['status'] == 0:
            num = num['code']
            tasks = [asyncio.ensure_future(self.download_csv(link,num)) for link in self.get_url(num)]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
        end = time.time()
        print('csv下载共运行了{}秒'.format(end-start))

        # 检查文件大小删除无效代码
        # csv_size.filesize_filter()

        self.csv_to_mongo()

    def csv_to_mongo(self):
        start = time.time()
        mycol = self.db['test_coll']
        count = 0
        fileList = os.listdir(self.filepath)
        # 依次对每个数据文件进行存储
        for fileName in tqdm(fileList):
            list = []
            with open(self.filepath + fileName,'r',encoding='gbk') as csvfile:
                data = csv.DictReader(csvfile)
                for each in data:
                    each['股票代码'] = each['股票代码'].strip('\'')
                    list.append(each)
                    count += 1
                mycol.insert_many(list)
        end = time.time()
        print('成功插入了{}条数据'.format(str(count)))
        print('存储到mongodb共运行了{}秒'.format(end-start))

if __name__ == '__main__':
    start = time.time()
    spider = Spider()
    # 'http://quote.eastmoney.com/stock_list.html'
    spider.run(get_code=0,get_code_url='http://quote.eastmoney.com/stock_list.html')
    print('爬取完成，共运行了{}秒'.format(time.time()-start))
    
