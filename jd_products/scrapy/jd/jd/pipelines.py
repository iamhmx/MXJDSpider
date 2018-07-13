# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem


class JdMongoDBPipeline(object):
    """
    当spider获取到item后，交到这里处理入库
    """
    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port
        self.mongodb = db
        self.collection = collection

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.mongodb]

    def close_spider(self, spider):
        self.client.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MONGODB_URL'),
            port=crawler.settings.get('MONGODB_PORT'),
            db=crawler.settings.get('MONGODB_DB'),
            collection=crawler.settings.get('KEYWORD')
        )

    def process_item(self, item, spider):
        """
        可以对item进行刷选、清理等操作
        :param item: 爬取到的item
        :param spider: 当前spider
        :return: item
        """
        if item['price'] is None:
            return DropItem('价格为None，丢弃')
        self.db[self.collection].insert(dict(item))
        return item
