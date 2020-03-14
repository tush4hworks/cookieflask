from flask import render_template, Flask, request, url_for, redirect, flash, make_response, jsonify, abort
from fetch_cookie import get_cookie, finder

app = Flask(__name__)



@app.route("/api/cookie", methods=['POST'])
def newcookie():
	username_finder = finder('name','username')
	password_finder = finder('name', 'password')
	button_finder = finder('xpath','//*[@type="submit"]')
	try:
		data = validate_request(request)
		if data.get('username_finder'):
			print("here")
			username_finder = finder(**data.get('username_finder'))
		if data.get('password_finder'):
			password_finder = finder(**data.get('password_finder'))
		if data.get('button_finder'):
			button_finder = finder(**data.get('password_finder'))

		fetched_cookies = get_cookie(data.get('baseurl'), data.get('username'), data.get('password'), username_finder, password_finder, button_finder)
		return jsonify(fetched_cookies)
	except Exception as e:
		abort(make_response(jsonify({"Exception":str(e)}), 400))

def validate_request(request):
	if not(request.json) or not all([request.json.get('baseurl'), request.json.get('username'), request.json.get('password')]):
		raise Exception("Invalid Input")
	return request.json


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)