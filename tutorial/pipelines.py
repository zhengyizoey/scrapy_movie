# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import MovieBriefItem
from helper import download_img
from db import db
import os


class MoviePipeline(object):
    def __init__(self, imgdir):
        if not os.path.exists(imgdir):
            os.mkdir(imgdir)
        self.imgdir = imgdir

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('IMG_DIR'))

    def process_item(self, item, spider):
        if isinstance(item, MovieBriefItem):
            movie_id = item['id']
            db['movie_brief'].update_one(
                {'id': movie_id},
                {'$set': dict(item)},
                upsert=True
            )
            img_path = os.path.join(self.imgdir, "{}.jpg".format(movie_id))
            download_img.delay(item['cover_url'], img_path)
        else:
            movie_id = item['id']
            db['movie_detail'].update_one(
                {'id': movie_id},
                {'$set': dict(item)},
                upsert=True
            )



