import redis

class DataStore:

	def __init__(self):
		self.r = redis.StrictRedis(host='localhost',port=6379,db=7)

	def insert(self,key,url_name,coupon_code,tweet,time):
		print "Entered Insert"
		self.r.sadd(url_name,key)

		self.r.hmset(key,{'tweet':tweet,'coupon_code':coupon_code})
		expiry_time = time
		self.r.expire(key,expiry_time)
		print "Successfully stored : " + url_name
		print " ---------------------------------- "
		print "Testing storage ......."
		self.fetch(url_name)

	def fetch(self,url_name):
		print "Entered fetch"
		if not self.r.exists(url_name):return False
		print self.r.smembers(url_name)
		result = []
		for x in self.r.smembers(url_name):
			if self.r.exists(x):
				result.append(self.r.hgetall(x))
			else:
				self.r.srem(url_name,x)
		print "Returning result for : " + url_name
		return result

	def delete(self,key):
		self.r.delete(key)

'''		
ds = DataStore()
ds.insert('a:1','a','xyz','aaaaaaaaaaa',60)
ds.insert('a:2','a','wxyz','aaaaaaaaaaa',50)
ds.insert('a:3','a','wxyz','aaaaaaaaaaa',50)
ds.delete('a:2')
ds.insert('b:1','b','vwxyz','aaaaaaaaaaa',40)

ds.fetch('a')
ds.fetch('b')
'''