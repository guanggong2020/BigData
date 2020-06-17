import aiohttp
import asyncio
from random import choice
import time
import pymongo
import os
import csv
from tqdm import tqdm

# 通过代码下载股票的历史交易记录并保存下来
class US_Spider(object):
    def __init__(self,SEM,US_CODE,US_PATH,US_DATA,START_TIME,END_TIME):
        self.USER_AGENT = [
                'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
                'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
                'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
                'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
                'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
                'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)',
            ]
        self.mycol = US_CODE
        self.sem = asyncio.Semaphore(SEM) #信号量，控制协程数
        self.filepath = US_PATH
        self.CODES = self.mycol.find({'status':0})
        self.DATA_COL = US_DATA
        self.START_TIME = START_TIME
        self.END_TIME = END_TIME

    async def get_content(self,link):
        async with self.sem:
            async with aiohttp.ClientSession() as session:# cookie字典在clientsession中自定义
                async with session.get(link,headers = {'User-Agent':choice(self.USER_AGENT)},timeout = 30) as rep:
                    content = await rep.read()
                    return content

    def get_url(self,code):
        start_time = self.START_TIME
        end_time = self.END_TIME
        url = f'https://www.nasdaq.com/api/v1/historical/{code}/stocks/{start_time}/{end_time}'
        yield url


    async def download_csv(self,link,code,name):
        condition = {'code': code}
        file_name = self.filepath + code + '_' + name + '.csv'
        try:
            content = await self.get_content(link)
            with open(file_name, 'wb') as f:
                f.write(content)
            print('下载成功 {}'.format(file_name))
            self.mycol.update_one(condition,{'$set':{'status':1}})
        except Exception as e:
            print(e)
            print('下载失败 {}'.format(file_name))
            # self.mycol.update_one(condition, {'$set': {'status':0}})

    def run(self):
        #下载csv文件
        start = time.time()
        for each in self.CODES:
            # if each['status'] == 0:
            code = each['code']
            name = each['name'].replace('/','&')
            tasks = [asyncio.ensure_future(self.download_csv(link,code,name)) for link in self.get_url(code)]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
        end = time.time()
        print('csv下载共运行了{}秒'.format(end-start))

        self.csv_to_mongo()

    def csv_to_mongo(self):
        start = time.time()
        mycol = self.db['historialstock']
        count = 0
        fileList = os.listdir(self.filepath)
        # 依次对每个数据文件进行存储
        for fileName in tqdm(fileList):
            list = []
            with open(self.filepath + fileName,'r',encoding='gbk') as csvfile:
                data = csv.DictReader(csvfile)
                try:
                    for each in data:
                        # print(each)
                        date = each['Date'].split('/')
                        dict = {
                            'date':f'{date[2]}-{date[0]}-{date[1]}',
                            'code':fileName.split('.')[0].split('_')[0],
                            'name':fileName.split('.')[0].split('_')[1].replace('&','/'),
                            'closingPrice':each[' Close/Last'].replace('$','').strip(),
                            'openingPrice': each[' Open'].replace('$', '').strip(),
                            'maxPrice': each[' High'].replace('$', '').strip(),
                            'minPrice': each[' Low'].replace('$', '').strip(),
                            'volume':each[' Volume'].strip()
                        }
                        list.append(dict)
                        count += 1
                    mycol.insert_many(list)
                except Exception as e:
                    print(e)

        end = time.time()
        print('成功插入了{}条数据'.format(str(count)))
        print('存储到mongodb共运行了{}秒'.format(end-start))
