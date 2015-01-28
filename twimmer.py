# -*- coding: utf-8 -*-

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from collections import OrderedDict
from utilities import Utilities
import json
import time
import pprint
import urllib

# OAUTH 

consumer_key ="2P8ti9KwJQcSlroJ61yaXJLTH"
consumer_secret = "8yfBybYC3IwYg8hclNJPnJRghNR7jsFMDQ93Ad3ma1esmGnvWw"
access_token = "100444884-wuvHF4Wxxnp5Sovp6zYQsN7kL4OSVFGvAWZdXXqJ"
access_token_secret = "UVOuGNQwOBDCPnTjvvDbhYuCk3YAVhoW65qWupZ0JDo3E"

words_to_track = ["coupon code","promo code"]

class listener(StreamListener):

	def __init__(self):
		self.recent_tweets = OrderedDict()

	def on_data(self,data):
		try:

			data = json.loads(data)
			newd = {}
			pprint.pprint(data)
			#print str(data['entities']['urls'])
			
			# Get Tweet
			s = Utilities.cleantweet(data['text'])
			if s in self.recent_tweets:
				return
			else:
				if len(self.recent_tweets) > 30:
					self.recent_tweets.popitem(last=False)
				self.recent_tweets[s] = True
			newd['tweet'] = s
			print s

			#print "got tweet"

			# Get Redirected url
			try:
				page = urllib.urlopen(str(data['entities']['urls'][0]['expanded_url']))
				newd['url'] = page.geturl()
			except:
				print "Url for tweet did not exist"
				print "----------------------------------------"
				return
			

			#Get timestamp
			newd['time'] = str(data['created_at'])

			#Get user description
			try:
				ud = Utilities.cleantweet(data['user']['description'])
				newd['userdesc'] = ud
			except:
				newd['userdesc'] = ""
				print "User description was not found"
				print "----------------------------------------"

			# Verify authenticity of website by checking if it has the word coupon
			# If it does , assume it is not a vendor site. Maybe blog, maybe coupon site

			url_name = str(newd['url'])

			if 'coupon' in url_name or 'facebook' in url_name or 'instagram' in url_name \
			or 'pinterest' in url_name or 'youtube' in url_name or 'tumblr' in url_name:
				newd['website'] = 'N'
				#Don't even store it in the file
				return
			else:
				newd['website'] = 'Y'
			#pprint.pprint(newd)
			

			# Create file and save data to it

			filename = 'DB' + str(time.strftime("%m%d")) +'.csv'

			saveFile = open(filename,'a')
			#print "opened file"
			#pprint.pprint(json.dumps(newd))
			saveFile.write(json.dumps(newd))
			#print "Finsihed writing to file"
			saveFile.write('\n')
			saveFile.close()
			print "----------------------------------------"
			return True
		except BaseException as e:
			print str(e)
			print "----------------------------------------"
			time.sleep(5)

	def on_error(self,status):
		try:
			print status
		except BaseException as e:
			print e
			time.sleep(1)


auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret) 

twitterStream = Stream(auth, listener())
twitterStream.filter(track=words_to_track)