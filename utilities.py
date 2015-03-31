# -*- coding: utf-8 -*-

import urllib

class Utilities:

	@staticmethod
	def trimquotes(s):

		if s == None or s == "":
			return s
		elif s[0] == '"' and s[-1] == '"':
			return s[1:-1]
		elif s[0] == "'" and s[-1] == "'":
			return s[1:-1]
		elif s[0] == "'" or s[0] == '"':
			#only preceeding quotes present
			return s[1:]
		elif s[-1] == "'" or s[-1] == '"':
			#only succeeding quotes present
			return s[:-1]
		else:
			return s

	@staticmethod
	def cleantweet(s):
		l = []
		#s = s.decode('unicode_escape')
		for c in  s:
			v = ord(c)
			if v <= 127 and v >= 0:
				l.append(c)

		return ''.join(l)

	@staticmethod
	def get_shortened_url(url_name,number = 5):

		count = 0
		last_seen = -1
		# 5 is ideal length by obseravation - after that, there is almost always crap!
		while count < number:
			last_seen = url_name.find('/',last_seen+1)
			if last_seen == -1 : return url_name
			count += 1
		return url_name[:last_seen+1]

	@staticmethod
	def get_redirected_url(url):
		page = urllib.urlopen(url)
		return page.geturl()

	@staticmethod
	def check_url_validity(url_name):
		if 'coupon' in url_name or 'facebook' in url_name or 'instagram' in url_name \
		or 'pinterest' in url_name or 'youtube' in url_name or 'tumblr' in url_name or 'twitter' in url_name:
			raise Exception('Not a useful url')

	@staticmethod
	def modify_url(url_name):
		all_urls = [url_name]
		if url_name[-1] == '/':
			all_urls.append(url_name[:-1])
		else:
			all_urls.append(url_name+'/')

		all_urls.append(Utilities.get_shortened_url(url_name,4))
		all_urls.append(Utilities.get_shortened_url(url_name,3))
		all_urls.append(Utilities.get_shortened_url(url_name,3)[:-1])

		return all_urls

#print Utilities.get_shortened_url('https://www.etsy.com/listing/122724402/sabrina-girl-dress-sewing-pattern-pdf?utm_source=Twitter&utm_medium=PageTools&utm_campaign=Share:::HEARTSRAIN')
#print cleantweet(u'\\n\\nSave 20% on LELO and PicoBong Pleasure Products\\nCoupon Code: LELOEF20\\nExpiry Date: 31 D... http://t.co/FiTyYlG4jC')
#print 'COUPON CODE➤ NOV16'.decode('unicode_escape').encode('ascii','ignore')
#print trimquotes("'hello'")
#print trimquotes('"hello"')
#print trimquotes('hello')