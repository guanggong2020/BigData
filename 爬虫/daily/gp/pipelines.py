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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataInsert')

class MongoDBPipeline(object):
    def __init__(self):
        # 连接池连接
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        self.GP_col = self.db[settings['MONGODB_GP_COL']]
        self.JJ_col = self.db[settings['MONGODB_JJ_COL']]
        # self.time = time.strftime("%Y-%m-%d", time.localtime())

    def process_item(self, item, spider):
        try:
            if item['data_type'] == 0: # 股票
                self.GP_col.insert_one(dict(item))
            else: # 基金
                self.JJ_col.insert_one(dict(item))
        except (Exception) as err:
            raise DropItem(err)
        return item
