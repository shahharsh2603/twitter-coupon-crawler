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

words_to_track = ["coupon code","promo code","discount code","etsy promo code","etsy coupon code"]

class listener(StreamListener):

	def __init__(self):
		self.recent_tweets = OrderedDict()
		self.tweets_with_coupons = 0
		self.tweets_with_dates = 0
		self.total_expiry_time = 0
		self.avg_expiry_time = 0

	def on_data(self,data):
		try:

			data = json.loads(data)
			newd = {}
			
			# Get Tweet
			tweet = Utilities.cleantweet(data['text'])
			
			for key in self.recent_tweets:
				#print Utilities.similarity(key,tweet)
				if Utilities.similarity(key,tweet) > 70:
					return
			'''
			if tweet in self.recent_tweets:
				return
			else:
			'''
			if len(self.recent_tweets) > 40:
				self.recent_tweets.popitem(last=False)
			self.recent_tweets[tweet] = True
			#print tweet

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
			if not code: 
				return
				raise BaseException("Did not have coupon code information")
			
			self.tweets_with_coupons += 1
			if not date : 
				date = 176800
			else :
				self.tweets_with_dates += 1
				self.total_expiry_time += date
				print date
				#print tweet
				#print " ----------------------------------- "
				#print "Tweet : ",
				
				#print "Url : ",
				#print url_name	
				#print "Date : "

			
			print "Coupons : " + str(self.tweets_with_coupons)
			print "Dates : " + str(self.tweets_with_dates)
			print "Total Expiry Time :" + str(self.total_expiry_time/3600) + "hours"
			print "Avg Expiry Time :" + str((self.total_expiry_time/(self.tweets_with_dates+1))/3600) + "hours"
			print '--------------------------------------'
			
			#print "CODE : " + code
			key = url_name + ':::' + code
			#print "KEY : " + key

			#print "Tweet : "
			print tweet
			#print "Url : ",
			#print url_name
			print " ----------------------------------- "
			
			ds = DataStore()
			#print url_name,code,date
			#get outer url - url uptil 3 '/'s . eg - http://www.etsy.com/
			outer_url = "parent::"+Utilities.get_shortened_url(url_name,3)
			ds.insert(key,url_name,code,tweet,date,outer_url)
			#print '-----------------------'

			return True
		except BaseException as e:
			if str(e) != "'text'":
				print " *************** " + str(e) + " *************** "
				print "----------------------------------------"
			time.sleep(1)

	def on_error(self,status):
		try:
			print status
		except BaseException as e:
			print e
			time.sleep(1)

def start_stream():
    while True:
        try:
            twitterStream = Stream(auth, listener())
            twitterStream.filter(track=words_to_track)
        except:
        	print " Broken Connection ! Attempting to reconnect . . ."
        	continue

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret) 

start_stream()