# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LandandresourceawardItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    asequence = scrapy.Field()
    pname = scrapy.Field()
    munit = scrapy.Field()
    mperson = scrapy.Field()
    anumber = scrapy.Field()
    awardtype = scrapy.Field()
    rank = scrapy.Field()
    type = scrapy.Field()
