from flask import g,Flask, redirect, url_for, render_template, flash, json, render_template_string
from flask import request, redirect, session, Blueprint
import requests
import json
import urllib
from ..helpers import auth_token
import bcrypt

val= getattr(g,'_app',None)

app = val.app



def check_username_existence(username):

	url = app.config["ERLANG_SERVER"] +"auth/check-username-existence/" + username
	data = {}
	data = json.dumps(data)
	headers = {}	
	response = requests.request("GET", url, headers=headers, params=data)
	return_value = response.text
	return return_value

# Usename Existence
@app.route('/is-username-registered/<username>',methods = ['GET'])
@auth_token.token_required
def username_exists(username):    
			
	exists = check_username_existence(username)
	if exists == "true":
		ret = {"success": True, "message": "Username already exists"}
		return json.dumps(ret)
	else:
		ret = {"success": False, "message": "Username does not exist"}
		return json.dumps(ret)


# Username creation
@app.route('/update-username', methods = ['POST'])
@auth_token.token_required
def update_username():    
	try:

		user_dict = json.loads(request.data.decode('utf-8'))

		username = user_dict["username"]

		exists = check_username_existence(username)

		if exists == "true":
			ret = {"success": False, "message": "Username already exists"}

		else:
			url = app.config["ERLANG_SERVER"] +"user/update-username/"
			data = urllib.parse.urlencode(user_dict)
			headers = {
				'content-type': "application/x-www-form-urlencoded",
				'cache-control': "no-cache",
				}
			response = requests.request("POST", url, headers=headers, data=data)
			return_value = json.loads(response.text)
			if "error" in return_value.keys():
				ret = {"success": False, "message": return_value["error"]}
				return json.dumps(ret)
			else:
				ret = {"success":True}
				return json.dumps(ret)
	
	except Exception as e:
		ret = {"success":False,"message":str(e)}
		return json.dumps(ret)


# Password updation
@app.route('/update-password', methods = ['POST'])
#@auth_token.token_required
def update_password():    
	try:

		user_dict = json.loads(request.data.decode('utf-8'))
		# password = bcrypt.hashpw(user_dict["password"].encode('utf-8', app.config.get('ROUND')), bcrypt.gensalt())
		# user_dict["password"] = password
		url = app.config["ERLANG_SERVER"] +"user/update-password/"
		data = urllib.parse.urlencode(user_dict)
		headers = {
			'content-type': "application/x-www-form-urlencoded",
			'cache-control': "no-cache",
			}
		response = requests.request("POST", url, headers=headers, data=data)
		return_value = json.loads(response.text)
		if "error" in return_value.keys():
			ret = {"success": False, "message": return_value["error"]}
			return json.dumps(ret)
		else:
			ret = {"success":True}
			return json.dumps(ret)
		
	except Exception as e:
		ret = {"success":False,"message":str(e)}
		return json.dumps(ret)





		