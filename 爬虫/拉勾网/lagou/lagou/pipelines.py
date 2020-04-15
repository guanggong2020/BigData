# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import redis
# from scrapy.conf import settings
from scrapy.exceptions import DropItem
# 新版本方法
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DataInsert')

class LagouPipeline(object):
    def __init__(self):
        # 连接池连接
        pool = redis.ConnectionPool(
            host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db=1)
        self.server = redis.Redis(connection_pool=pool)

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
        self.MONGODB_COL = self.db[settings['MONGODB_COL']]

    def process_item(self, item, spider):
        try:
            key = 'filter_' + item['positionId']
            if self.server.get(key) is None:
                self.server.set(key, "save")
                self.MONGODB_COL.insert(dict(item))
        except (Exception) as err:
            raise DropItem(err)

        return item

