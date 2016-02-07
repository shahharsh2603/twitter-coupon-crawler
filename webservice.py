from flask import Flask,jsonify,request
from utilities import Utilities
from datastore import DataStore
import redis

app = Flask(__name__)

@app.route('/',methods=['POST'])
def get_tasks():
	u = request.form['url'].lower()
	
	url = Utilities.get_shortened_url(u)
	url_3 = Utilities.get_shortened_url(u,3)

	return_only_parent = False

	# If url is same as parent url, return everything just for parent
	# Dont redundantly return for parent and itself
	if url == url_3 or url+'/' == url_3:
			return_only_parent = True

	ds = DataStore()

	if not return_only_parent:

		all_urls = Utilities.modify_url(url)
		print all_urls

		# If the same url is also a parent url, return all results of parent .
		# And skip individual url results

		for url in all_urls:
			result = ds.fetch(url)
			if result == False:
				print " Tried for url " + url
			else:
				x = {"result":result}
				return jsonify(x)

	# If for our exact url and its modifications , nothing got returned

	outer_url = "parent::" + Utilities.get_shortened_url(url,3)
	print outer_url
	
	result = ds.fetch_all_from_parent(outer_url)
	if result : 
		x = {"result":result}
		return jsonify(x)
	else:
		if outer_url[-1] == '/':
			result = ds.fetch_all_from_parent(outer_url[:-1])
		else:
			result = ds.fetch_all_from_parent(outer_url + '/')
		if result : 
			x = {"result":result}
			return jsonify(x)

	# If there is still nothing to show
	return 'No Response'

if __name__ == '__main__':
    app.run(debug=True)