from flask import g,Flask, redirect, url_for, render_template, flash, json, render_template_string
from flask import request, redirect, session, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
	current_user
#from flask_login import LoginManager, UserMixin, login_user, logout_user
import flask
import requests
import json
import urllib	
#from flask import logout_user

val= getattr(g,'_app',None)

app = val.app


def check_email_existence(email):

	url = app.config["ERLANG_SERVER"] +"auth/check-email-existence/" + email
	data = {}
	data = json.dumps(data)
	headers = {}		
	response = requests.request("GET", url, headers=headers, params=data)
	return_value = response.text
	return return_value



def check_domain_existence(domain):

	url = app.config["ERLANG_SERVER"] +"auth/check-domain-existence/" + domain
	data = {}
	data = json.dumps(data)
	headers = {}		
	response = requests.request("GET", url, headers=headers, params=data)
	return_value = response.text
	return return_value

# Email Signup
@app.route('/signup', methods = ['POST'])
def sign_up():    
	try:

		mydict = json.loads(request.data.decode('utf-8'))

		email = mydict["email"]
		domain = mydict["domain"]

		exists = check_email_existence(email)

		if exists == "true":

			ret = {"success": True, "message": "email already exists"}
			return json.dumps(ret)

		else:

			url = app.config["ERLANG_SERVER"] +"auth/add-user/"
			data = urllib.parse.urlencode({"email": email, "domain": domain, "is_email_verified": "false", "status": "active", "user_agent":str(request.user_agent)})
			print (data)
			headers = {
				'content-type': "application/x-www-form-urlencoded",
				'cache-control': "no-cache",
				}
			#return_value = "success"
			response = requests.request("POST", url, headers=headers, data=data)
			return_value = response.text
			if return_value == "success":
				ret = {"success":True,"message": "signup successful"}
				return json.dumps(ret)
			else:			
				ret = {"success": False}
				return json.dumps(ret)


		
		
	except Exception as e:
		ret = {"success":False,"message":str(e)}
		return json.dumps(ret)


@app.route('/add-domain', methods = ['POST'])
def add_domain():    
	try:

		mydict = json.loads(request.data.decode('utf-8'))

		domain = mydict["domain"]
		is_public = mydict["is_public"]

		exists = check_domain_existence(domain)

		if exists == "true":

			ret = {"success": True,"message": "domain already exists"}
			return json.dumps(ret)

		else:
				
			url = app.config["ERLANG_SERVER"] +"auth/add-domain/"
			data = urllib.parse.urlencode({"domain_name": domain, "is_public": is_public})
			headers = {
				'content-type': "application/x-www-form-urlencoded",
				'cache-control': "no-cache",
				}
			#return_value = "success"
			response = requests.request("POST", url, headers=headers, data=data)
			return_value = response.text
			if return_value == "success":
				ret = {"success":True,"message": "Domain created successfully"}
				return json.dumps(ret)
			else:			
				ret = {"success": False}
				return json.dumps(ret)

		
		
	except Exception as e:
		ret = {"success":False,"message":str(e)}
		return json.dumps(ret)



# Email Existence
@app.route('/is-email-registered/<email>',methods = ['GET'])
def email_exists(email):    
	
		exists = check_email_existence(email)
		if exists == "true":
			ret = {"success": True, "message": "email already exists"}
			return json.dumps(ret)
		else:
			ret = {"success":False, "message": "email does not exist"}
			return json.dumps(ret)



# Email Verified
@app.route('/is-email-verified/<email>',methods = ['GET'])
def email_verified(email):    
	
		print (email)
		
		url = app.config["ERLANG_SERVER"] +"auth/is-email-verified/" + email
		print (url)
		data = {}
		data = json.dumps(data)
		headers = {}		
		response = requests.request("GET", url, headers=headers, params=data)
		return_value = response.text
		print("Here", return_value)
		if return_value == "true":
			ret = {"success": True,"message": "email is verified"}
			return json.dumps(ret)
		else:
			ret = {"success": False,"message": "email is not verified"}
			return json.dumps(ret)
		


# Domain Existence
@app.route('/is-domain-registered/<domain>',methods = ['GET'])
def domain_exists(domain):    
	
		exists = check_domain_existence(domain)

		if exists == "true":
			ret = {"success": True,"message": "domain already exists"}
			return json.dumps(ret)
		else:
			ret = {"success": False,"message": "domain does not exist"}
			return json.dumps(ret)



# Usename Existence
@app.route('/is-username-registered/<username>',methods = ['GET'])
def username_exists(username):    
	
		print ("username")
		
		url = app.config["ERLANG_SERVER"] +"auth/check-username-existence/" + username
		print ("url")
		data = {}
		data = json.dumps(data)
		headers = {}	
			
		response = requests.request("GET", url, headers=headers, params=data)
		return_value = response.text
		
		'''
		return_value = {"success":"true"}
		'''
		if return_value == "true":
			ret = {"success": True, "message": "Username already exists"}
			return json.dumps(ret)
		else:
			ret = {"success": False, "message": "Username does not exist"}
			return json.dumps(ret)

		


# Secret Code for Email Verification
@app.route('/verification-code/<email>',methods = ['GET'])
def verification_code(email):

		print ("verification_code")


		url = app.config["ERLANG_SERVER"] +"auth/generate-email-verification-code/" + email
		print ("url")
		data = {}
		data = json.dumps(data)
		headers = {}		
		response = requests.request("GET", url, headers=headers, params=data)
		return_value = response.text
		print(return_value)
		# Send email here
		ret = {"success": True, "message": "Verification code has been sent to your registered email"}
		return json.dumps(ret)
		
		 

# Secret code for login
@app.route('/login-code/<username>',methods = ['GET'])
def login_code(username):

		print ("login-code")

		url = app.config["ERLANG_SERVER"] +"/login-code/" + username
		print ("url")
		data = {}
		data = json.dumps(data)
		headers = {}		
		response = requests.request("GET", url, headers=headers, params=data)
		return_value = json.loads(response.text)
		if return_value["success"] == "true":
			ret = {"success":"true","message": "Login code accepted"}
			return json.dumps(ret)
		else:
			ret = {"success":"false","message": "Incorrect login code"}
			return json.dumps(ret)




# Email login
@app.route('/login',methods = ["POST"])
def log_in():    
	try:

		mydict = json.loads(request.data)

		email = mydict["email"]
		username = mydict["username"]
		password = mydict["password"]
		code = mydict["code"]
		print("email", "username", "password", "code")
		
		url = app.config["ERLANG_SERVER"] +"auth/login"
		print("url")
		data = {"email": email, "username": "username", "password":password, "code":code}
		data = json.dumps(data)
		headers = {}
		response = requests.request("POST", url, headers=headers, data=data)
		return_value = json.loads(response.text)
		if return_value["success"] == "true":
			ret = {"success":"true","message": "Login successful", "token":"token"}
			return json.dumps(ret)
		else:
			ret = {"success":"false","message":str(e)}
			return json.dumps(ret)

		
		
	except Exception as e:
		ret = {"success":"false","message":str(e)}
		return json.dumps(ret)



# Email Verification
@app.route('/verify-email',methods = ["POST"])
def verify_email():    
	try:

		mydict = json.loads(request.data.decode('utf-8'))

		email = mydict["email"]
		verification_code = mydict["verification_code"]
		print(email, verification_code)
		
		url = app.config["ERLANG_SERVER"] + "auth/verify-email"
		print(url)
		data = urllib.parse.urlencode({"email": email, "code":verification_code})
		headers = {
		'content-type': "application/x-www-form-urlencoded",
			'cache-control': "no-cache",
		}
		response = requests.request("POST", url, headers=headers, data=data)
		return_value = response.text
		print(return_value)
		if return_value == "true":
			ret = {"success": True,"message": "Email verified successfully"}
			return json.dumps(ret)
		else:
			ret = {"success": False,"message":"Email can't be verified"}
			return json.dumps(ret)
		
	except Exception as e:
		ret = {"success": False,"message":str(e)}
		return json.dumps(ret)












