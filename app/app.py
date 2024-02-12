from flask import Flask, request, make_response, jsonify, abort

from fetch_cookie import get_cookie, finder
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/api/cookie", methods=['POST'])
def newcookies():
    try:
        return jsonify(try_get_cookie(request))
    except Exception as e:
        abort(make_response(jsonify({"Exception": str(e)}), 400))


@app.route("/api/cookie/<cookiename>", methods=['POST'])
def newcookie(cookiename):
    try:
        return jsonify(try_get_cookie(request, cookie_filter=cookiename))
    except Exception as e:
        abort(make_response(jsonify({"Exception": str(e)}), 400))


def validate_request(request):
    if not (request.json) or not all(
            [request.json.get('baseurl'), request.json.get('username'), request.json.get('password')]):
        raise Exception("Invalid Input:baseurl, username and password are mandatory")
    return request.json


def try_get_cookie(request, cookie_filter=None):
    username_finder = finder('name', 'username')
    password_finder = finder('name', 'password')
    button_finder = finder('xpath', '//*[@type="submit"]')
    fullname_finder = finder(None, None)
    data = validate_request(request)
    if data.get('username_finder'):
        username_finder = finder(**data.get('username_finder'))
    if data.get('password_finder'):
        password_finder = finder(**data.get('password_finder'))
    if data.get('button_finder'):
        button_finder = finder(**data.get('button_finder'))
    if data.get("fullname_finder"):
        fullname_finder = finder(**data.get("fullname_finder"))
    fetched_cookies = get_cookie(data.get('baseurl'), data.get('username'), data.get('password'), username_finder,
                                 password_finder, button_finder, fullname_finder, cookie_filter)
    return fetched_cookies


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
