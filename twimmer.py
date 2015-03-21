# -*- coding: utf-8 -*-

import json
import time
import pprint
import urllib
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from collections import OrderedDict
from utilities import Utilities
from extractMethods import Extraction
from datastore import DataStore

# OAUTH 

consumer_key ="2P8ti9KwJQcSlroJ61yaXJLTH"
consumer_secret = "8yfBybYC3IwYg8hclNJPnJRghNR7jsFMDQ93Ad3ma1esmGnvWw"
access_token = "100444884-wuvHF4Wxxnp5Sovp6zYQsN7kL4OSVFGvAWZdXXqJ"
access_token_secret = "UVOuGNQwOBDCPnTjvvDbhYuCk3YAVhoW65qWupZ0JDo3E"

words_to_track = ["coupon code","promo code","discount code"]

class listener(StreamListener):

	def __init__(self):
		self.recent_tweets = OrderedDict()

	def on_data(self,data):
		try:

			data = json.loads(data)
			newd = {}
			
			# Get Tweet
			tweet = Utilities.cleantweet(data['text'])
			
			if tweet in self.recent_tweets:
				return
			else:
				if len(self.recent_tweets) > 30:
					self.recent_tweets.popitem(last=False)
				self.recent_tweets[tweet] = True
				print tweet

			# Get Redirected url
			try:
				url_name = Utilities.get_redirected_url(str(data['entities']['urls'][0]['expanded_url']))
			except:
				return
				raise BaseException("Url for tweet did not exist")
			
			# Get shortened url for key --> Upto 5th '/' or entire address (whichever is shorter)

			url_name = Utilities.get_shortened_url(url_name).lower()

			#Get timestamp
			timestamp = str(data['created_at'])

			# Verify authenticity of website by checking if it has the word coupon
			# If it does , assume it is not a vendor site. Maybe blog, maybe coupon site

			try:
				Utilities.check_url_validity(url_name)
			except:
				return
				raise BaseException("Url was not a valid site")
			
			# Code to extract important information from this tweet

			e = Extraction()
			code,date = e.extract_all(tweet)
			if not date : date = 86400
			else :
				date = 86400
				#print "Tweet : ",
				#print tweet
				#print "Url : ",
				#print url_name	
				#print "Date : " , 
				#print date
				#print " ----------------------------------- "
				pass

			if not code: 
				return
				raise BaseException("Did not have coupon code information")
			
			print "CODE : " + code
			key = url_name + ':::' + code
			print "KEY : " + key

			print "Tweet : ",
			print tweet
			print "Url : ",
			print url_name
			#print " ----------------------------------- "

			ds = DataStore()
			#print url_name,code,date
			ds.insert(key,url_name,code,tweet,date)
			#print '-----------------------'

			return True
		except BaseException as e:
			print " *************** " + str(e) + " *************** "
			print "----------------------------------------"
			time.sleep(2)

	def on_error(self,status):
		try:
			print status
		except BaseException as e:
			print e
			time.sleep(2)

def start_stream():
    while True:
        try:
            twitterStream = Stream(auth, listener())
            twitterStream.filter(track=words_to_track)
        except:
        	print " SCRIPT CRASHED "
        	continue

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret) 

start_stream()