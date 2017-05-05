# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieBriefItem(scrapy.Item):
    id = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    cover_url = scrapy.Field()


class MovieDetailItem(scrapy.Item):
    id = scrapy.Field()  # 电影I
    ratings_on_weight = scrapy.Field()  # 评分占比：5星到1星[34.5, 23, 1, 0.2, 45]
    summary = scrapy.Field()  # 电影简介
    recommendations_bd = scrapy.Field()  # 相似电影

