import redis
import time
import sys
from datastore import DataStore
r = redis.StrictRedis(host='localhost',port=6379,db=7)
#r.flushall()
print r.dbsize()
#url = sys.argv[1]
#ds = DataStore()
#print ds.dbsize()
#ds.fetch(url)