import json
import pprint
import sys
import random
from optparse import OptionParser
from extractMethods import Extraction
		

class TweetData:

	def __init__(self,filename):
		self.coupon_data = dict()
		self.url_code_lookup = dict()
		self.sample_dictionary = dict()
		self.filename = filename

	def check_codes(self):

		readFile = open(self.filename,'r')

		e = Extraction()
		count1 = 0 
		count2 = 0
		for line in readFile:
			data = json.loads(line)
			url = str(data['url'])
			tweet = str(data['tweet'])
			e.set_tweet_value(tweet)
			#print tweet
			code = e.extract_code_regex_1()	#Coupon Code, Promo Code
			#print output
			code = e.extract_code_regex_2() if not code else code #Code :
			#print output
			code = e.extract_code_regex_3() if not code else code #Code ABCD :
			#print code
			#print "---------------------------------------------------------"
			date = e.extract_date()

			#building the url lookup dictionary

			if url in self.url_code_lookup:
				if code:
					if code not in self.url_code_lookup[url]:
						self.url_code_lookup[url].append(code)
			else:
				if code:
					self.url_code_lookup[url] = [code]

			#building the coupon data dictionary

			if code in self.coupon_data:
				#Add to dictionary only if the code is for a url that's not already present
				if url not in self.coupon_data[code][0][1]:
					self.coupon_data[code].append((tweet,url))
			else:
				self.coupon_data[code]= [(tweet,url,date)]

		#print count1,count2
		return len(self.coupon_data)

	def display(self):
		#pprint.pprint(self.coupon_data)
		pprint.pprint(self.url_code_lookup)

	def get_percentage_dates(self):
		count1 = 0
		count2 = 0
		for key in self.sample_dictionary:
			if self.sample_dictionary[key][0][2] != None:
				count1+=1
			count2+=1

		return (count1*100)/count2,count1,count2

	def num_unique_codes(self):
		return len(self.coupon_data) - 1

	def num_unique_urls(self):
		return len(self.url_code_lookup)

	def random_sample(self,k):

		print len(self.coupon_data)
		keys = random.sample(self.coupon_data,k)
		for key in keys:
			if key: 
				# When the key is not None
				self.sample_dictionary[key] = self.coupon_data[key]
				value = self.sample_dictionary[key]
				'''
				if value[0][2] != None :
					print value[0][2] + " : " + value[0][0] + " : " + key
				'''
				print '"' + key + '"' + ':' + value[0][0]
				#print value[0][1]
				print value[0][2]
				print "--"

	def search(self,url):
		if url in self.url_code_lookup:
			return self.url_code_lookup[url][0]
		else:
			return "Url not found"
				

def parse_options():
	op = OptionParser()
	k = 0
	op.add_option('-s','--samplesize',dest = 'k',action = 'store')
	options,args = op.parse_args()
	if options.k :
		k = options.k
	return int(k)

if __name__ == '__main__':
	
	td = TweetData(sys.argv[1])
	n = td.check_codes()
	k = parse_options()
	
	if k != 0:
		td.random_sample(k)
	else:
		td.random_sample(n)
	
	print td.get_percentage_dates()
	print "Codes " + str(td.num_unique_codes())
	print "URLS " + str(td.num_unique_urls())
	td.display()
	#print td.search(raw_input())
	#td.random_sample(1300)
	
