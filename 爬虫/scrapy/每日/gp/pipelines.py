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
        # 用户验证
        # connection.admin.authenticate(
        #     settings['MONGODB_USER'],
        #     settings['MONGODB_PW']
        # )
        self.db = connection[settings['MONGODB_DB']]
        self.GP_col = self.db[settings['MONGODB_GP_COL']]
        self.JJ_col = self.db[settings['MONGODB_JJ_COL']]
        self.SH_col = self.db[settings['MONGODB_SH_COL']]
        self.SZ_col = self.db[settings['MONGODB_SZ_COL']]
        # self.time = time.strftime("%Y-%m-%d", time.localtime())

    def process_item(self, item, spider):
        try:
            if item['data_type'] == 0: # 股票
                self.GP_col.insert_one(dict(item))
            elif item['data_type'] == 1: # 基金
                self.JJ_col.insert_one(dict(item))
            elif item['data_type'] == 2: # 上证
                self.SH_col.insert_one(dict(item))
            else:
                self.SZ_col.insert_one(dict(item))
        except (Exception) as err:
            raise DropItem(err)
        return item
