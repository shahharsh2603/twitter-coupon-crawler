import sys
import random
import difflib
import csv
from extractMethods import Extraction

def randomsample(filename,size):

	with open(filename,'r') as f:

		x = []
		t = ""

		for line in f.readlines():

			if line[:2] == "--":
				if t != "":
					x.append(t)
				t = ""
			else:
				if line !=  "" :
					t += line
		
	return random.sample(x,int(size))

def get_tweet_sample(filename,size):

	tweets = randomsample(filename,size)
	to_remove = set()
	for i in xrange(len(tweets)):
		for j in xrange(i+1,len(tweets)):
			if j not in to_remove:
				if (difflib.SequenceMatcher(None,tweets[i].lower(),tweets[j].lower()).ratio()) * 100 > 60:
					to_remove.add(j)

	ans = [i for j,i in enumerate(tweets) if j not in to_remove]
	return ans,len(ans)

def write_to_csv(ans):
	e = Extraction()
	with open("resultExpiry.csv",'w') as wf:
		fieldnames = ["TWEET","MANUAL COUPON CODE","MANUAL EXPIRY","EXTRACTED COUPON CODE","EXTRACTED EXPIRY"]
		writer = csv.DictWriter(wf,delimiter = ',',fieldnames = fieldnames)
		writer.writeheader()
		#writer.writeheader("TWEET","MANUAL COUPON CODE","MANUAL EXPIRY","EXTRACTED COUPON CODE","EXTRACTED EXPIRY")
		for tweet in ans:
			code,time = e.extract_all(tweet)
			if time:
				time = int(time)/3600

			writer.writerow({'TWEET':tweet,'MANUAL COUPON CODE':None,'MANUAL EXPIRY':None,'EXTRACTED COUPON CODE':code,'EXTRACTED EXPIRY':time})
			#writer.writerow([tweet,None,None,code,time])

	wf.close()

if __name__ == '__main__':
	x,y = get_tweet_sample(sys.argv[1],sys.argv[2])
	print y
	if y > 300:
		write_to_csv(x)
	#print randomsample(sys.argv[1],sys.argv[2])
