from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import urllib

import requests
import pymongo
import selenium

import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.dupefilters
import scrapy.squeues

import scrapy.extensions.spiderstate
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.logstats
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.feedexport
import scrapy.extensions.closespider
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.extensions.throttle

import scrapy.core.scheduler
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.core.downloader

import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.chunked
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt

import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength

import scrapy.pipelines

import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory


list = ['dataspider','stockspider','DailyFunds','fundspider']
print('输入需要获取的数据类型：')
print('1--当日国内数据，2--当日美股数据，3--当日美国基金数据，4--历史美国基金数据\n',
      '--------------------------------------------------------------')
Flag = True
while Flag:
      num = int(input())
      if num not in [1,2,3,4]:
            print('输入错误，请重试:')
      else:
            Flag = False
            process = CrawlerProcess(get_project_settings())
            process.crawl(list[num-1])
            process.start()

# from scrapy.cmdline import execute
# import sys
# import os
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy","crawl",list[int(num)-1]])
#
# print(sys.argv[0],sys.argv[1])



