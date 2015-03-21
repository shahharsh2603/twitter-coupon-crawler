from flask import Flask,jsonify,request
from utilities import Utilities
from datastore import DataStore
import redis

app = Flask(__name__)

r = redis.StrictRedis(host='localhost',port=6379,db=7)

@app.route('/',methods=['POST'])
def get_tasks():
	u = request.form['url']
	url = Utilities.get_shortened_url(u)
	all_urls = Utilities.modify_url(url)
	ds = DataStore()
	for url in all_urls:
		result = ds.fetch(url)
		if result == False:
			print " Tried for url " + url
		else:
			x = {"result":result}
			return jsonify(x)

	return 'No Response'

if __name__ == '__main__':
    app.run(debug=True)