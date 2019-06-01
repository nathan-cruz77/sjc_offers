# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo import ReplaceOne


class MongoPipeline(object):

    collection_name = 'offers'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'app')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.operations = []

    def close_spider(self, spider):
        self.flush_operations()
        self.client.close()

    def process_item(self, item, spider):
        d_item = dict(item)
        op = ReplaceOne(d_item, d_item, upsert=True)
        self.operations.append(op)

        if len(self.operations) >= 1000:
            self.flush_operations()

        return item

    def flush_operations(self):
        if self.operations:
            self.db[self.collection_name].bulk_write(self.operations)

        self.operations = []
