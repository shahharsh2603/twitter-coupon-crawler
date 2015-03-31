from datetime import datetime
from datetime import timedelta
import re

class ExpirySetter:

	days_in_months = {
	'January':(1,31),
	'February':(2,28),
	'March':(3,31),
	'April':(4,30),
	'May':(5,31),
	'June':(6,30),
	'July':(7,31),
	'August':(8,31),
	'September':(9,30),
	'October':(10,31),
	'November':(11,30),
	'December':(12,31)
	}

	oneday = timedelta(hours = 23,minutes = 59,seconds = 59)

	@staticmethod
	def formatIdentifier(datestring,year = ''):

		# Will take default format as mm/dd/yyyy
		separator = ''
		if '-' in datestring:
			separator = '-'
		elif '/' in datestring:
			separator = '/'

		date = datestring.split(separator)
		month = int(date[0])
		day = int(date[1])
		if year == '':
			year = int(date[2])
		d = '%d'
		m = '%m'
		y = '%Y'
		# Not a month
		if month > 12:
			d = '%m'
			m = '%d'

		if year < 99:
			y ='%y'
		
		format = m+separator+d+separator+y
		return format,separator

	@staticmethod
	def setExpiryFromDate3(datestring):
		
		current_time = datetime.now()
		format,separator = ExpirySetter.formatIdentifier(datestring)
		end_time = datetime.strptime(datestring,format)
		end_time = end_time + ExpirySetter.oneday
		#end_time.day += 1

		#Difference between expiry date and current time
		x = int((end_time - current_time).total_seconds())
		return x if x > 0 else None

	@staticmethod
	def setExpiryFromDate2(datestring):

		current_time = datetime.now()
		year = str(current_time.year)
		format,separator = ExpirySetter.formatIdentifier(datestring,year)
		#print format, separator
		#print datestring + separator + str(year)
		end_time = datetime.strptime(datestring+separator+year,format)
		end_time = end_time + ExpirySetter.oneday

		#Difference between expiry date and current time
		x = int((end_time - current_time).total_seconds())
		return x if x > 0 else None


	@staticmethod
	def matchMonth(month):

		re_m = re.compile('Jan(uary)?',re.IGNORECASE)
		if re_m.match(month):
			return 'January'
		re_m = re.compile('Feb(ruary)?',re.IGNORECASE)
		if re_m.match(month):
			return 'February'
		re_m = re.compile('Mar(ch)?',re.IGNORECASE)
		if re_m.match(month):
			return 'March'
		re_m = re.compile('Apr(il)?',re.IGNORECASE)
		if re_m.match(month):
			return 'April'
		re_m = re.compile('May',re.IGNORECASE)
		if re_m.match(month):
			return 'May'
		re_m = re.compile('June?',re.IGNORECASE)
		if re_m.match(month):
			return 'June'
		re_m = re.compile('July?',re.IGNORECASE)
		if re_m.match(month):
			return 'July'
		re_m = re.compile('Aug(ust)?',re.IGNORECASE)
		if re_m.match(month):
			return 'August'
		re_m = re.compile('Sept?(ember)?',re.IGNORECASE)
		if re_m.match(month):
			return 'September'
		re_m = re.compile('Oct(ober)?',re.IGNORECASE)
		if re_m.match(month):
			return 'October'
		re_m = re.compile('Nov(ember)?',re.IGNORECASE)
		if re_m.match(month):
			return 'November'
		re_m = re.compile('Dec(ember)?',re.IGNORECASE)
		if re_m.match(month):
			return 'December'

		return None


	#To handle datestrings of type 'April', 'march 31','June 2016' etc

	@staticmethod
	def setExpiryFromMonthAndDate(datestring):

		current_time = datetime.now()
		
		date = datestring.split()

		month = ExpirySetter.matchMonth(date[0])
		# Getting date on the basis of regex matching the month
		# So if month not found, no point doing anything else.
		# It will probably be wrong

		if not month:return None

		month_number = ExpirySetter.days_in_months[month][0]


		if len(date) > 2:
			year = int(date[2])
		else:
			year = int(current_time.year)

		if len(date) > 1:
			# If date is something like April 12-15, we want to extract 15 as day value
			# because that is what will be the end date
			if '-' in date[1]:
				x = date[1].split('-')	
				day = int(x[1])
			else:
				day = int(date[1])

			if day > ExpirySetter.days_in_months[month][1]:
				# It probably is representing year and not day
				# For example , April 2015
				# Set april 2015 to 4-30-2015
				year = day
				day = ExpirySetter.days_in_months[month][1]					

		else:
			#Set to last day of month
			day = ExpirySetter.days_in_months[month][1]

		new_datestring = str(month_number) + '-' + str(day) + '-' + str(year)
		#print "new datestring : " + new_datestring

		return ExpirySetter.setExpiryFromDate3(new_datestring)

	@staticmethod
	def setExpiryFromKeyword(keyword):
		re_k = re.compile('\s?((to|2)day|(to|2)night)',re.IGNORECASE)
		if re_k.match(keyword):
			current_time = datetime.now()
			datestring = str(current_time.month) + '-' + str(current_time.day) + '-' + str(current_time.year)
			#print datestring
			return ExpirySetter.setExpiryFromDate3(datestring)

		re_k = re.compile('\s?(2|to)mor?ro?w',re.IGNORECASE)
		if re_k.match(keyword):
			current_time = datetime.now()
			end_time = current_time + ExpirySetter.oneday
			datestring = str(end_time.month) + '-' + str(end_time.day) + '-' + str(end_time.year)
			#print datestring
			return ExpirySetter.setExpiryFromDate3(datestring)

		re_k = re.compile('\s?(Mon(day)?|Tuesday|Wednesday|Thursday|Friday)',re.IGNORECASE)
		if re_k.match(keyword):
			current_time = datetime.now()
			end_time = datetime(current_time.year,current_time.month,current_time.day,23,59,59)
			count = 0 # To avoid infinite loop
			while keyword.strip().lower() != end_time.strftime("%A").lower() and count < 8:
				end_time += ExpirySetter.oneday
				count += 1
			x = int((end_time - current_time).total_seconds())
			return x if x > 0 else None 


#print ExpirySetter.setExpiryFromMonthAndDate('April 2015')
#print ExpirySetter.setExpiryFromKeyword('TODAY')
#print ExpirySetter.setExpiryFromKeyword('2MORW')
#print ExpirySetter.setExpiryFromMonthAndDate(u'mar 12-31')
#print ExpirySetter.setExpiryFromDate2('30/4')
#print ExpirySetter.setExpiryFromDate2('4/30')
#print ExpirySetter.setExpiryFromDate3('4/30/15')
#print ExpirySetter.setExpiryFromDate3('4/30/2015')
#print ExpirySetter.setExpiryFromKeyword('tUesDaY')
#print ExpirySetter.setExpiryFromKeyword('wednesdaY')
#print ExpirySetter.setExpiryFromKeyword('monDaY')
#print ExpirySetter.setExpiryFromKeyword(' thursdaY')
'''
print ExpirySetter.matchMonth('Jan')
print ExpirySetter.matchMonth('feb')
print ExpirySetter.matchMonth('march')
print ExpirySetter.matchMonth('jun')
print ExpirySetter.matchMonth('JUL')
print ExpirySetter.setExpiryFromDate2('3/31')
print ExpirySetter.setExpiryFromDate3('3/31/2016')
print ExpirySetter.setExpiryFromDate3('20150325')
'''