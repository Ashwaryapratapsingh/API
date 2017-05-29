from flask import g, request
from functools import wraps
import json
import jwt

val= getattr(g,'_app',None)
app = val.app

def token_required(f):
	@wraps(f)
	def token_validation(*args, **kwargs):
		auth_header = request.headers.get('Authorization')
		if auth_header:
			auth_token = auth_header.split(" ")[1]
		else:
			auth_token = ''
		if auth_token:
			try:
				payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
				g.user = payload
				return f(*args, **kwargs)
			except Exception as e:
				return json.dumps({"success": False, "authorized": False, "message": "Failed to authorize request123123"})
		else:
			return json.dumps({"success": False, "authorized": False, "message": "No token supplied123213"})

	return token_validation


def tokenize(payload):
	token = jwt.encode(
	        payload,
	        app.config.get('SECRET_KEY'),
	        algorithm='HS256'
	    )

	return token













