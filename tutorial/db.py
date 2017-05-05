# coding=utf-8
import pymongo

HOST = "127.0.0.1"
PORT = 27017
DB_NAME = 'scrapymovie'

client = pymongo.MongoClient(HOST, PORT)
db = client[DB_NAME]
