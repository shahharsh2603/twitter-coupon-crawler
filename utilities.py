# -*- coding: utf-8 -*-
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

#print cleantweet(u'\\n\\nSave 20% on LELO and PicoBong Pleasure Products\\nCoupon Code: LELOEF20\\nExpiry Date: 31 D... http://t.co/FiTyYlG4jC')
#print 'COUPON CODE➤ NOV16'.decode('unicode_escape').encode('ascii','ignore')
#print trimquotes("'hello'")
#print trimquotes('"hello"')
#print trimquotes('hello')