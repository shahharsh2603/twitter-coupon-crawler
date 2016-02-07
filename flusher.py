import redis

p = 6379
i = 1
r = redis.StrictRedis(host='localhost',port=6379,db=1)
r.flushall()
print "Successfully flushed database " + str(i) + " on port " + str(p)