# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MafengwoItem(scrapy.Item):
    source = scrapy.Field()  # 来源
    second_source = scrapy.Field()  # 二级来源
    remark_acccount = scrapy.Field()  # 评论数
    scene_name = scrapy.Field()  # 景点名称
    remarks = scrapy.Field()  # 评论，包含评论内容和评论时间字段
