# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import requests
from random import choice
import logging

from scrapy.http import HtmlResponse as Response
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataSpider')

# 异步网络框架，作用：从远程加载url数据时不堵塞主线程
from twisted.internet import defer,reactor
# reactor.suggestThreadPoolSize(32) #线程池大小32
# https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list

class RandomUserAgent(object):
    def __init__(self, agents):
        # 使用初始化的agents列表
        self.agents = agents
        self.cookies = 'adBlockerNewUserDomains=1583116092; __gads=ID=6c24cb69fd33c42a:T=1583116095:S=ALNI_MYl1wN41zMFyD_qfyzhswOdmMFhQg; _ga=GA1.2.78373687.1583116095; r_p_s_n=1; _fbp=fb.1.1583758013522.2132325212; __atuvc=2%7C10%2C1%7C11; PHPSESSID=5hn4nv2vi4ni1uq0ppk2oqs5fr; geoC=CN; comment_notification_210005407=1; prebid_page=0; prebid_session=0; StickySession=id.24079475795.328cn.investing.com; _gid=GA1.2.1868315375.1585217825; Hm_lvt_a1e3d50107c2a0e021d734fe76f85914=1585103366,1585116226,1585116292,1585217826; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A7%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228873%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Findices%2Fus-30-futures%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228258%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A25%3A%22%2Fequities%2Fchesapeake-ener%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22998179%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A41%3A%22%2Ffunds%2Ft.-rowe-price-capital-appreciation%22%3B%7Di%3A3%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22997364%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A33%3A%22%2Ffunds%2Fvanguard-500-index-admiral%22%3B%7Di%3A4%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A7%3A%221049656%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A42%3A%22%2Ffunds%2Fstate-street-sp-500-index-securitii%22%3B%7Di%3A5%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A7%3A%221047115%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A42%3A%22%2Ffunds%2Fks-schwab-moderately-aggressive-ind%22%3B%7Di%3A6%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22991848%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A30%3A%22%2Fequities%2Fmorningstar-japan-kk%22%3B%7D%7D%7D%7D; ses_id=Mnw2d2doMDg0cGxqYTA1NmAxZD8zNGViYWRmZWRkZHI2ImRqYTZlIz8wbyFgYzQoMTc1YWFjM2c8OW40OjczZDI%2BNjZnMDA4NGtsZ2EyNTBgOGRuM2dlZmEzZmNkN2RrNjRkZmExZWM%2FaG9nYGA0OzEjNSlhJTMiPG5uPjp7M3QyPTZ3ZzQwOTRlbDNhOjU1YGJkODM3ZWRhZ2Y0ZGdkfDZ9; nyxDorf=MTVkNm8%2FPnw%2Faz02Yi80NGIwNWs2LzMzYmIzNA%3D%3D; Hm_lpvt_a1e3d50107c2a0e021d734fe76f85914=1585218251'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENT_CHOICES'))

    @defer.inlineCallbacks
    def process_request(self,request,spider):
        container=[]
        '''
        实际进行远程读取操作的是_get_res,所以process_request不会堵塞主线程，而是直接返回.
        另外，reactor是事件管理器，用于注册、监控、处理、注销事件，事件发生时调用回调函数处理。
        callInThread创建了指定断点运行的函数以及传递变量的挂起线程，之后通过reactor.run()来启动

        在yield一个deferred对象之后，主函数就会中断在此处，等待callback完成信号传入再往下运行，直到
        returnValue处deferred获得结果
        '''
        out=defer.Deferred()
        '''
        Deferred对象主要有callback和errback两个方法，
        当耗时操作完成后执行callback或errback（错误时）方法，告诉Deferred对象工作已完成
        '''
        reactor.callInThread(self._get_res, request, container, out)
        yield out
        if len(container)>0:
            defer.returnValue(container[0])

    def _get_res(self,request,container,out):
        try:
            _header = {
                "Cookie": self.cookies,
                "User-Agent": choice(self.agents),
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

            _url = request.url

            if _url in ['https://cn.investing.com/instruments/HistoricalDataAjax']:
                req = requests.post(url=_url, headers=_header, data=request.meta['params'])
                req.encoding = 'utf-8'
                response = Response(url=req.url, status=req.status_code, body=req.content,
                                    encoding=request.encoding, request=request)

            else:
                req = requests.get(url=_url, headers=_header)
                req.encoding = 'utf-8'
                response = Response(url=req.url, status=req.status_code, body=req.content,
                                    encoding=request.encoding, request=request)

            container.append(response)
            reactor.callFromThread(out.callback, response)#传出response

        except Exception as e:
            err = str(type(e)) + ' ' +str(e)
            reactor.callFromThread(out.errback, ValueError(err))

    def process_response(self,response,request,spider):

        return response

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


# class FundsDownloaderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
