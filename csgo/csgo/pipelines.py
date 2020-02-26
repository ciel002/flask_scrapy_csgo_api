# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from csgo.items import B5Item, A5EItem
from csgo.models import init_sqlalchemy, B5Model, A5EModel


class B5Pipeline(object):
    def __init__(self):
        super(B5Pipeline, self).__init__()
        self.session = init_sqlalchemy()

    def process_item(self, item, spider):
        if isinstance(item, B5Item):
            self.session.add(B5Model(**item))
            self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()


class A5EPipeline(object):
    def __init__(self):
        super(A5EPipeline, self).__init__()
        self.session = init_sqlalchemy()

    def process_item(self, item, spider):
        if isinstance(item, A5EItem):
            self.session.add(A5EModel(**item))
            self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
