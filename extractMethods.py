import re
import json
import pprint
import urllib
import stopwords
from utilities import Utilities
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

		code = re.sub(regExRemove,'',answer)

		#trimquotes
		code = Utilities.trimquotes(code)

		if code.isdigit() or code == '' or code.lower() in stopwords.stopwords:
			return 

		return code


	def extract_code_regex_1(self):
		#regex for coupon code and promo code
		regex = re.compile('#?(Coupon|Promo)\s-??#?Code,?\s?:?\s?,?\*?\'?"?[A-Z0-9_-]{3,20}\'?"?',re.IGNORECASE)
		regex2 = re.compile('#?(Coupon|Promo)\s-??#?Code,?\s?:?\s?,?\*?',re.IGNORECASE)

		return self.extract_code(regex,regex2)

	def extract_code_regex_2(self):
		#regex for code :
		regex = re.compile('Code\s?:\s?[A-Z0-9_]{3,20}',re.IGNORECASE)
		regex2 = re.compile('Code\s?:\s?',re.IGNORECASE)

		return	self.extract_code(regex,regex2) 

	def extract_code_regex_3(self):
		#regex for code followed by CAPITAL CODE
		regex = re.compile('(code|CODE|Code)\s?:?\s?[A-Z0-9_]{3,20}')
		regex2 = re.compile('Code\s?:?\s?',re.IGNORECASE)

		return	self.extract_code(regex,regex2)

	def extract_date(self):

		regExMain = re.compile('(\d+[-/\.]\d+[-/\.]\d+)')
		exp = re.findall(regExMain,self.tweet)
		if not exp: 
			regExMain = re.compile('(\d+/\d+)')
			exp = re.findall(regExMain,self.tweet)
		if not exp:
			regex1 = re.compile('(|Expires|before|at|on|until|thru|through|ends|exp|is)\s?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept?|Oct|Nov|Dec)\.?\s?\d+',re.IGNORECASE)
			regex2 = re.compile('(Expires|before|at|on|until|thru|through|ends|exp|is)\s?',re.IGNORECASE) 
			exp = [self.extract_code(regex1,regex2)]
		if exp == None or exp[0] == None:
			#Space in front to avoid finding friday from BLACKFRIDAY
			regExMain = re.compile('\s(tomorrow|today|tonight|2day|Monday|Tuesday|Wednesday|Thursday|Friday)',re.IGNORECASE)
			exp = re.findall(regExMain,self.tweet)
			#if exp: print exp[-1], self.tweet
		if not exp:return None
		date = exp[-1]
		return date

