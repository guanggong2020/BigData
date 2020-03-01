# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo
import time
# from scrapy.conf import settings
from scrapy.exceptions import DropItem
# 新版本方法
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import scrapy
import urllib.request as ur
from random import choice

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataInsert')
time = time.strftime("%Y-%m-%d",time.localtime())

class MongoDBPipeline(object):
    def __init__(self):
        # 连接池连接
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        self.col = self.db[settings['MONGODB_COL']]

    def process_item(self, item, spider):
        try:
            item['date'] = time
            self.col.insert_one(dict(item))# 记得将item转为字典类型，否则插入出错
        except (Exception) as err:
            raise DropItem(err)
        return item
