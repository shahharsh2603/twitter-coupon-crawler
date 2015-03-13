from flask import Flask,jsonify,request
from utilities import Utilities
from datastore import DataStore
import redis

app = Flask(__name__)

r = redis.StrictRedis(host='localhost',port=6379,db=7)
info = {"Size":r.dbsize()}
r.set("Hey",1)
@app.route('/',methods=['POST'])
def get_tasks():
	u = request.form['url']
	url = Utilities.get_shortened_url(u)
	x = {"url":url}
	return jsonify(x)

if __name__ == '__main__':
    app.run(debug=True)