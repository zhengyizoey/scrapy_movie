# coding=utf-8
import sys
from scrapy import cmdline
if sys.getdefaultencoding() != 'gbk':
    reload(sys)
    sys.setdefaultencoding('gbk')

cmdline.execute('scrapy crawl moviespider'.split())