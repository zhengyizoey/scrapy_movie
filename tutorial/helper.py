# coding=utf-8

import random
import celery
import logging
import requests
from settings import IMG_DIR
from fake_useragent import UserAgent

app = celery.Celery('img_task', broker='redis://localhost')
logger = logging.Logger(__name__)
SAMPLE = range(97, 123)+range(65, 90)+range(48, 57)+[95, 45]
BID_LEN = 11
BIDS_NUM = 500

def gen_bids():
    bids = []
    for i in range(BIDS_NUM):
        bid = ''.join(chr(i) for i in random.sample(SAMPLE, BID_LEN))
        bids.append(bid)
    return bids

def gen_ua():
    ua = UserAgent()
    return ua.random

@app.task
def download_img(imgurl, imgpath):
    try:
        response = requests.get(imgurl)
        with open(imgpath, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        logging.warning('failed to download {}'.format(imgurl))



