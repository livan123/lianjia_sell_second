# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    #一页多少房子
    ii = scrapy.Field()
    #url：
    url = scrapy.Field()
    #标题：
    title = scrapy.Field()
    #房型：
    typess = scrapy.Field()
    #位置：
    location = scrapy.Field()
    #总价：
    total_price = scrapy.Field()
    #单价：
    price = scrapy.Field()
    #房屋概况：
    basic_facts = scrapy.Field()



