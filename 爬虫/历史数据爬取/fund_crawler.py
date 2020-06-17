import aiohttp
import asyncio
from random import choice
from tqdm import tqdm
from lxml import etree
import requests

class FUND_Spider(object):
    def __init__(self,SEM,FUND_CODE,START_TIME,END_TIME,FUND_DATA):
        self.USER_AGENT = [
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
            'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
            'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
            'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)',
        ]

        self.sem = asyncio.Semaphore(SEM)  # 信号量，控制协程数
        self.CODES = FUND_CODE.find().limit(10)
        self.START_TIME = START_TIME
        self.END_TIME = END_TIME
        self.DATA_COL = FUND_DATA

    async def get_content(self, link):
        async with self.sem:
            async with aiohttp.ClientSession() as session:  # cookie字典在clientsession中自定义
                async with session.get(
                        link,
                        headers={
                            'User-Agent': choice(self.USER_AGENT)},
                        timeout=30) as rep:
                    content = await rep.text()
                    pageHTML = etree.HTML(content)
                    return pageHTML

    def get_url(self, num):
        start_time = self.START_TIME
        end_time = self.END_TIME

        url = f'http://quotes.money.163.com//fund/jzzs_{num}_0.html?start={start_time}&end={end_time}'
        res = requests.get(url=url, headers={'User-Agent': choice(self.USER_AGENT)}, timeout=10)
        res.encoding = 'utf8'
        html = res.text
        pageHTML = etree.HTML(html)
        page = pageHTML.xpath('//a[@class="pages_flip"]/preceding-sibling::a/text()')
        if page != []:
            for i in range(int(page[-1])):
                if i == int(page[-1])-1:
                    condition = {'code': num}
                    # .update_one(condition,{'$set':{'status':0}})
                url = f'http://quotes.money.163.com//fund/jzzs_{num}_{i}.html?start={start_time}&end={end_time}'
                yield url
        else:
            yield 0

    async def analy_page(self, link, num ):
        data_list = []
        if link == 0:
            print(f'代码 {num} 该基金历史交易为空')
            # self.mycol.remove({"code":num})
        else:
            try:
                content = await self.get_content(link)
                title = content.xpath('//small/a/text()')
                time = content.xpath('//tbody/tr/td[1]/text()')
                dwjz = content.xpath('//tbody/tr/td[2]/text()')
                ljjz = content.xpath('//tbody/tr/td[3]/text()')
                zzr = content.xpath('//tbody/tr/td[4]/span/text()')

                for each in range(len(time)):
                    dic = {
                        '基金名称':title[0],
                        '时间':time[each],
                        '单位净值':dwjz[each],
                        '累计净值':ljjz[each],
                        '增长率':zzr[each]
                    }
                    data_list.append(dic)
                self.data_to_mongo(data_list)
            except Exception as e:
                print(e)

    def run(self):
        for num in tqdm(self.CODES):
            if num['status'] == 1:
                num = num['code']
                tasks = [asyncio.ensure_future(self.analy_page(link, num)) for link in self.get_url(num)]
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.wait(tasks))

    def data_to_mongo(self,data_list):
        mycol = self.DATA_COL
        mycol.insert_many(data_list)
        # print('{}条数据已插入'.format(str(len(data_list))))

