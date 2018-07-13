# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    """
    定义商品信息字段（id，标题，图片地址，价格，评论数，店铺）
    """
    pid = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    commit = scrapy.Field()
    shop = scrapy.Field()

    def show(self):
        # 不能用self.id
        print('id：', self['pid'])
        print('名称：', self['title'])
        print('图片：', self['image'])
        print('价格：', self['price'])
        print('评论数：', self['commit'])
        print('店铺：', self['shop'])
        print('='*100)
