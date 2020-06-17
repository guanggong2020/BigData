# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from random import choice
import logging
from scrapy.http import HtmlResponse
import time
from datetime import date,timedelta
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataSpider')

# https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list

class RandomUserAgent(object):
    def __init__(self, agents):
        # 使用初始化的agents列表
        self.agents = agents
        self.today = date.today()
        self.yesterday = date.today() + timedelta(days=-1)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENT_CHOICES'))

    def process_request(self,request,spider):
        request.headers.setdefault('User-Agent', choice(self.agents))
        request.headers.setdefault('accept-Encoding', 'gzip, deflate, br')
        request.headers.setdefault('accept-language', 'zh-CN,zh;q=0.9,ja;q=0.8')
        request.headers.setdefault('connection', 'keep-alive')
        request.headers.setdefault('cache-control', 'max-age=0')
        request.headers.setdefault('upgrade-insecure-requests', '1')
        request.headers.setdefault('accept',
                                   'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3')

    def process_response(self,response,request,spider):

        if request.url in ['http://quote.eastmoney.com/center/gridlist.html#us_stocks']:
            spider.bro.get(url=request.url)
            time.sleep(2)  # 一定要给与浏览器一定的缓冲加载数据的时间
            page_text = spider.bro.page_source
            # 篡改响应对象
            return HtmlResponse(url=spider.bro.current_url, body=page_text, encoding='utf-8', request=request)
        else:
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

        # Should return either None or an iterable of Response, dict
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