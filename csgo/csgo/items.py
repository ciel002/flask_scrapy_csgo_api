# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class CsgoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class B5Item(scrapy.Item):
    map = scrapy.Field()
    url = scrapy.Field()
    steamId = scrapy.Field()
    score = scrapy.Field()
    time = scrapy.Field()
    kda = scrapy.Field()
    result = scrapy.Field()
    rws = scrapy.Field()
    rating = scrapy.Field()
    damage = scrapy.Field()
    adr = scrapy.Field()
    headshot = scrapy.Field()
    awp = scrapy.Field()
    firstKill = scrapy.Field()


class A5EItem(scrapy.Item):
    map = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    score = scrapy.Field()
    time = scrapy.Field()
    kda = scrapy.Field()
    result = scrapy.Field()
    rws = scrapy.Field()
    rating = scrapy.Field()
    damage = scrapy.Field()
    adr = scrapy.Field()
    headshot = scrapy.Field()
    awp = scrapy.Field()
    firstKill = scrapy.Field()
