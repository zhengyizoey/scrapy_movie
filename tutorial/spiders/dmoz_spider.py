# coding=utf-8
import scrapy
from tutorial.items import MovieBriefItem, MovieDetailItem
import logging
import json
import urlparse

logger = logging.getLogger(__name__)


class MovieSpider(scrapy.Spider):
    name = 'moviespider'
    # allowed_domains = ['https://movie.douban.com']
    # count_url = "https://movie.douban.com/j/chart/top_list_count?type=24&interval_id=90:80"
    # start_urls = ["https://movie.douban.com/j/chart/top_list?type=24&interval_id=100:90&action=&start=20&limit=20"]

    def __init__(self, types, interval_id, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        self.types = types
        high, low = interval_id
        self.interval_ids = [str(i)+':'+str(i-10) for i in range(high, low-1, -10) if i>low]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(types=crawler.settings.get('TYPES'), interval_id=crawler.settings.get('INTERVAL_ID'))

    def start_requests(self):
        base_count_url = "https://movie.douban.com/j/chart/top_list_count?type={}&interval_id={}"
        for type_ in self.types:
            for interval_id in self.interval_ids:
                url = base_count_url.format(type_, interval_id)
                yield scrapy.Request(url=url, callback=self.parse_count)

    def parse_count(self, response):
        json_body = json.loads(response.body_as_unicode())
        base_ajax_url = "https://movie.douban.com/j/chart/top_list?action=&start={}&limit={}"
        total = json_body['total']
        start = 0
        limit = 20
        while total > start:
            logging.info('- ----------start parse_count')
            url = base_ajax_url.format(start, limit)+'&'+response.url.split('?')[1]
            yield scrapy.Request(url=url, callback=self.parse_content)
            start += 20

    def parse_content(self, response):
        logger.warning('start start++++++++++++ moviesoider , parse content response')
        json_body = json.loads(response.body_as_unicode())
        for i in json_body:
            item = MovieBriefItem()
            item['id'] = i['id']
            item['title'] = i['title']
            item['rating'] = i['rating']
            item['url'] = i['url']
            item['cover_url'] = i['cover_url']
            yield item
            yield scrapy.Request(url=i['url'], callback=self.parse_page)


    def parse_page(selfs, response):
        id = response.url.split('/')[4]
        ratings_on_weight = []
        path = '//div[@class="ratings-on-weight"]/div[{}]/span[@class="rating_per"]/text()'
        for i in range(1, 6):
            ratings_on_weight.append(response.xpath(path.format(i)).extract_first())
        summary = response.xpath(r'//span[@property="v:summary"]//text()').extract_first()
        dls = response.xpath('.//div[@class="recommendations-bd"]/dl')
        recommendations_bd = []
        for dl in dls:
            href = dl.xpath('.//dd/a/@href').extract_first()
            recommendations_bd.append(href)
        item = MovieDetailItem()
        item['id'] = id
        item['ratings_on_weight'] = ratings_on_weight
        item['summary'] = summary
        item['recommendations_bd'] = [url.split('/')[4] for url in recommendations_bd]
        yield item




