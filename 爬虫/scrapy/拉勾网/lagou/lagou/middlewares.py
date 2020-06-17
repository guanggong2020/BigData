# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from random import choice
from scrapy.http import HtmlResponse as Response
from twisted.internet import defer,reactor
import requests
import json
import copy
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataSpider')

class LagouDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, agents):
        self.agents = agents
        self.stage = [
                '%E6%9C%AA%E8%9E%8D%E8%B5%84',
                '%E5%A4%A9%E4%BD%BF%E8%BD%AE',
                'A%E8%BD%AE',
                'B%E8%BD%AE',
                'C%E8%BD%AE',
                'D%E8%BD%AE%E5%8F%8A%E4%BB%A5%E4%B8%8A',
                '%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8',
                '%E4%B8%8D%E9%9C%80%E8%A6%81%E8%9E%8D%E8%B5%84'
            ]
        self.cookie = \
        'JSESSIONID=ABAAAECABBJAAGI20346CDE4282F6FDC1FD9F159BAF03F1; user_trace_token=20200412180912-65f5ba02-741f-4a0e-8a92-dad90f73212a; WEBTJ-ID=20200412180912-1716ddd4e7d4bf-082f3e1e42a0ec-5313f6f-1296000-1716ddd4e7eb7; X_HTTP_TOKEN=f8edbabcef5d9490251686685140a6386b41961463; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist%5FPython%2Fp-city%5F0-jd%5F2%3Fpx%3Ddefault%23filterBox; LGSID=20200412180912-0535384d-b0d9-414c-a243-c483790ff49c; PRE_SITE=; LGUID=20200412180912-207952ad-dd5c-4418-ae6f-54eea14b6268; _ga=GA1.2.1929526146.1586686153; _gat=1; _gid=GA1.2.1187236200.1586686153; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221716ddd515f3f7-0886732ae3497e-5313f6f-1296000-1716ddd5161139%22%2C%22%24device_id%22%3A%221716ddd515f3f7-0886732ae3497e-5313f6f-1296000-1716ddd5161139%22%7D; sajssdk_2015_cross_new_user=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1586686153; LGRID=20200412180913-ad8febd6-9df7-478b-8b1b-f621277ab251; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1586686153; SEARCH_ID=e7203d6902ec472aadfcfdfd8802e878'

        self.zhima_API = \
        'http://http.tiqu.alicdns.com/getip3?num=20&type=2&pro=0&city=0&yys=100017&port=11&pack=92232&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=440000&gm=4'

        self.proxy_ip = []
        for each in json.loads(requests.get(
                url=self.zhima_API,
                headers={
                    "User-Agent": 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
            ).text)['data']:
            self.proxy_ip.append(each['ip'] + ':' + str(each['port']))


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings.getlist('USER_AGENT_CHOICES'))

    @defer.inlineCallbacks
    def process_request(self, request, spider):
        container = []
        '''
        Deferred对象主要有callback和errback两个方法，
        当耗时操作完成后执行callback或errback（错误时）方法，告诉Deferred对象工作已完成
        '''
        out = defer.Deferred()
        '''
        实际进行远程读取操作的是_get_res,所以process_request不会堵塞主线程，而是直接返回.
        另外，reactor是事件管理器，用于注册、监控、处理、注销事件，事件发生时调用回调函数处理。
        callInThread创建了指定断点运行的函数以及传递变量的挂起线程，之后通过reactor.run()来启动

        在yield一个deferred对象之后，主函数就会中断在此处，等待callback完成信号传入再往下运行，直到
        returnValue处deferred获得结果
        '''
        reactor.callInThread(self._get_res, request, container, out)
        yield out
        if len(container) > 0:
            defer.returnValue(container[0])

    def _get_res(self, request, container, out):
        _url = request.url
        response = {}
        try:
            if request.meta['method'] == "start":
                _header = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Connection': 'keep-alive',
                    'Origin': 'https://www.lagou.com',
                    'Referer': 'https://www.lagou.com/',
                    "User-Agent": choice(self.agents),
                    "Host": "www.lagou.com",
                    "Cookie": self.cookie
                }
                req = requests.get(url=_url, headers=_header)
                req.encoding = 'utf-8'
                response = Response(url=req.url, status=req.status_code, body=req.content,
                                    encoding=request.encoding, request=request)

            if request.meta['method'] == "page":
                while True:
                    times = 5

                    user_agent = choice(self.agents)
                    # _ip = json.loads(requests.get('http://localhost:5010/get/').text)['proxy']
                    proxies = {'https': choice(self.proxy_ip)}

                    try:
                        home_url = request.url
                        home_resp = requests.get(
                            url=home_url,
                            headers={
                                'Accept': 'application/json, text/javascript, */*; q=0.01',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'Accept-Language': 'zh-CN,zh;q=0.8',
                                'Connection': 'keep-alive',
                                'Origin': 'https://www.lagou.com',
                                'Referer': 'https://www.lagou.com/',
                                'user-agent': user_agent,
                                "Host": "www.lagou.com"
                                # "Cookie": self.cookie,cookie会帮助反爬虫机制识别爬虫
                            },
                            proxies=proxies,
                            timeout=10)
                        cookies = home_resp.cookies.get_dict()

                        params = request.meta['params']
                        params['sid'] = cookies['SEARCH_ID']

                        num = request.meta['stage']

                        if request.meta['isSchooljobs'] == '0':
                            post_url = \
                                f'https://www.lagou.com/jobs/positionAjax.json?jd={self.stage[num]}&px=default&needAddtionalResult=false'
                        else:
                            post_url = \
                                f'https://www.lagou.com/jobs/positionAjax.json?jd={self.stage[num]}&px=default&needAddtionalResult=false&isSchoolJob=1'

                        req = requests.post(
                            url=post_url,
                            headers={
                                'user-agent': user_agent,
                                'X-Anit-Forge-Token': None,
                                'X-Anit-Forge-Code': '0',
                                'X-Requested-With': 'XMLHttpRequest',
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Referer': request.meta['referer_URL']
                            },
                            proxies = proxies,
                            data=params,
                            cookies=cookies,
                            timeout=10
                        )
                        req.encoding = 'utf-8'
                        response = Response(url=req.url, status=req.status_code, body=req.content,
                                            encoding=request.encoding, request=request)

                        if req.status_code == 200:
                            break
                    except Exception as e:
                        logger.debug(e)
                    times = times - 1
                    if times == 0:
                        break

            container.append(response)
            reactor.callFromThread(out.callback, response)  # 传出response

        except Exception as e:
            err = str(type(e)) + ' ' + str(e)
            reactor.callFromThread(out.errback, ValueError(err))


    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



