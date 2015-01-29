import redis
import time
import sys
from datastore import DataStore
#r = redis.StrictRedis(host='localhost',port=6379,db=7)

url = sys.argv[1]
ds = DataStore()
ds.fetch(url)