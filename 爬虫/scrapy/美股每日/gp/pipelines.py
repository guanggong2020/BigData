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
        connection.admin.authenticate(
            settings['MONGODB_USER'],
            settings['MONGODB_PW']
        )
        self.db = connection[settings['MONGODB_DB']]
        self.col = self.db[settings['MONGODB_DAILY_COL']]

    def process_item(self, item, spider):
        try:
            key = dict(item)
            del key['num']
            self.col.insert_one(key)
        except (Exception) as err:
            raise DropItem(err)
        return item
