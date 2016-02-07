import redis

class DataStore:

	def __init__(self):
		self.r = redis.StrictRedis(host='localhost',port=6379,db=4)

	def insert(self,key,url_name,coupon_code,tweet,time,outer_url):
		#print "Entered Insert"
		self.r.sadd(url_name,key)
		
		self.r.hmset(key,{'tweet':tweet,'coupon_code':coupon_code})
		expiry_time = time
		self.r.expire(key,expiry_time)

		#Add url to set of all the urls in its outer url
		self.r.sadd(outer_url,url_name)
		#print url_name + " was added to " + outer_url
		#print "Database size: " + str(self.r.dbsize())
		#print "Successfully stored : " + url_name
		#print " ---------------------------------- "
		#print "Testing storage ......."
		#self.fetch(url_name)

	def fetch(self,url_name):
		print "Entered fetch"
		#self.r.flushall()
		#print "Successfully flushed"
		if not self.r.exists(url_name): return False
		print self.r.smembers(url_name)
		result = []
		for x in self.r.smembers(url_name):
			if self.r.exists(x):
				record = self.r.hgetall(x)
				record['expiry'] = '%.1f' % (float(self.r.ttl(x))/(3600*24))
				result.append(record)
			else:
				self.r.srem(url_name,x)
		print "Returning result for : " + url_name
		return result

	def delete(self,key):
		self.r.delete(key)

	def fetch_all_from_parent(self,outer_url):
		print "Entered here - parent function"
		if not self.r.exists(outer_url): return False
		total_result = []
		for x in self.r.smembers(outer_url):
			print "x : " + str(x)
			if self.r.exists(x):
				total_result.append(self.fetch(x))
			else:
				self.r.srem(outer_url,x)
		result = [x for y in total_result for x in y]
		print result
		return result


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