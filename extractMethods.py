import re
import json
import pprint
import urllib
import stopwords
from utilities import Utilities
from expirySetter import ExpirySetter
import sys

class Extraction:

	def __init__(self):
		self.tweet = None

	def set_tweet_value(self, myTweet):
		self.tweet = myTweet

	def extract_code(self,regExMain,regExRemove):

		#expression with coupon code
		exp = re.search(regExMain,self.tweet)

		if not exp: return None

		#if pattern match was found, remove words 'coupon code' and extract just the code
		answer = exp.group(0)
		answer = ' '.join([word for word in answer.split() if word.lower() not in stopwords.stopwords])
		if 'Expires' in answer or 'ends' in answer:
			print answer

		code = re.sub(regExRemove,'',answer)

		#trimquotes
		code = Utilities.trimquotes(code)

		if code.isdigit() or code == '' or code.lower() in stopwords.stopwords:
			return 

		return code


	def extract_code_regex_1(self):
		#regex for coupon code,discount code and promo code
		regex = re.compile('#?(Coupon|Promo|Discount)\s-??#?Code,?\s?:?\s?,?\*?\'?"?[A-Z0-9_-]{3,20}\'?"?',re.IGNORECASE)
		regex2 = re.compile('#?(Coupon|Promo|Discount)\s-??#?Code,?\s?:?\s?,?\*?',re.IGNORECASE)

		return self.extract_code(regex,regex2)

	def extract_code_regex_2(self):
		#regex for code , but not product code:
		regex = re.compile('(?!Product)Code\s?:\s?\'?"?[A-Z0-9_]{3,20}\'?"?',re.IGNORECASE)
		regex2 = re.compile('Code\s?:\s?',re.IGNORECASE)

		return	self.extract_code(regex,regex2) 

	def extract_code_regex_3(self):
		#regex for code followed by CAPITAL CODE but not product code
		regex = re.compile('(?!Product)(code|CODE|Code)\s?:?\s?\'?"?[A-Z0-9_]{3,20}\'?"?')
		regex2 = re.compile('Code\s?:?\s?',re.IGNORECASE)

		return	self.extract_code(regex,regex2)

	def extract_code_regex_4(self):
		#regex for CAPITAL CODE followed by coupon code etc
		regex = re.compile('\'?"?[A-Z0-9_]{3,20}\'?"?\s?#?((C|c)oupon|(P|p)romo|(D|d)iscount)\s-?#?(code|CODE|Code)')
		regex2 = re.compile('\s?#?(Coupon|Promo|Discount)\s#?Code\s?',re.IGNORECASE)

		return	self.extract_code(regex,regex2)

	def extract_date(self):

		regExMain = re.compile('([0-9]+[-/][0-9]+[-/][0-9]+)')
		exp = re.findall(regExMain,self.tweet)
		if exp:
			#print exp
			return ExpirySetter.setExpiryFromDate3(exp[-1])

		if not exp:
			regExMain = re.compile('([0-9]+/[0-9]+)')
			exp = re.findall(regExMain,self.tweet)
			if exp: 
				#print exp
				return ExpirySetter.setExpiryFromDate2(exp[-1])

		if not exp:
			regex1 = re.compile('(Expires|before|at|until|thru|through|ends|exp|is|ending|exp\.|to|by)\s?(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|June?|July?|Aug(ust)?|Sept?(ember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\.?\s?[0-9]+[!\.]?',re.IGNORECASE)
			regex2 = re.compile('(Expires|before|at|until|thru|through|ends|exp|is|ending|exp\.|to|by)\s?',re.IGNORECASE)
			exp = [self.extract_code(regex1,regex2)]
			if exp and exp[0] != None:
				#print exp
				return ExpirySetter.setExpiryFromMonthAndDate(exp[-1])
			
		if exp == None or exp[0] == None:
			#Space in front to avoid finding friday from BLACKFRIDAY
			regExMain = re.compile('\s(tom(orrow)?|(to|2)day|(to|2)night|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)!?\.?\s?',re.IGNORECASE)
			exp = re.search(regExMain,self.tweet)
			#print "ALL : ",
			#print exp
			if exp:
				#print exp.group(0)
				#print self.tweet
				x = ExpirySetter.setExpiryFromKeyword(str(exp.group(0)))
				return x
		if not exp:return None
		date = exp[-1]
		return date

	def extract_all(self,tweet):

		self.set_tweet_value(tweet)
		code = self.extract_code_regex_1()	#Coupon Code, Promo Code
		code = self.extract_code_regex_2() if not code else code #Code :
		code = self.extract_code_regex_3() if not code else code #Code ABCD :
		code = self.extract_code_regex_4() if not code else code
		try:
			date = self.extract_date()
		except:
			date = None

		return code,date

e = Extraction()
#print e.extract_all("Clemson Alumni Night is on April 13 at the Hornets vs. Houston Rockets game! Order by April 3! using promo code:TIGERS http://t.co/26bWDIMaej")
# print e.extract_all('April 1st thru April 31st Finally Its Spring 20 discount on all artwork. Use the discount code NHVPKY  http://t.co/dVx5B0x3qG')
# print e.extract_all("RT @Real_BabyLux: Get 20% off anything from http://t.co/tavYS6UKeZ with the discount code OTRA1D20 EXPIRES TODAY http://t.co/2z5SUO2oaN")
# print e.extract_all("*VIP OFFER* Get 20% off all bookings for Friday, just enter the promo code PRYZMFRIDAY20 on checkout! http://t.co/LeojLwoIxg")
# print e.extract_all("CCB Ticket Flash Sale running now through 11:59 PM April 1st. Tickets are $130 ($45 savings) promo code MARCHMEALS http://t.co/4tkrLteylA")
# print e.extract_all("Product Code: B00ECMTXPA Rating: 4.5/5 stars List Price: $ 148.00 Discount: Save $ 10 http://t.co/jzmnOeSRJX http://t.co/bh9iDKVpc5")
#print e.extract_all("Three Rocks (5X7) - Free Shipping - Other sizes available - 10OFF Promo code gets you 10percent off! https://t.co/xfbV1UrJx9 #Etsy #Pond")
#print e.extract_all("RT @RealLionMaker: Use the code 'LIONMAKER' and get 15 Discount on any item in EU US stores. ENDS MONDAY. http://t.co/bSV3FrelL")
print e.extract_all("2.25 x 74 Until April 16! #thermalpaper for new #Verifone VX520 #terminal use LAROCCA3 code for discount http://t.co/k2pC9ATluV http://t.co/BwFhzUFAC7")