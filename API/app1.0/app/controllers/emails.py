from flask import g,Flask, redirect, url_for, render_template, flash, json, render_template_string
from flask import request, redirect, session, Blueprint
import requests
import json
import urllib
from ..helpers import auth_token

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


@app.route('/add-domain', methods = ['POST'])
@auth_token.token_required
def add_domain():    
	try:

		mydict = json.loads(request.data.decode('utf-8'))

		domain = mydict["domain_name"]

		exists = check_domain_existence(domain)

		if exists == "true":

			ret = {"success": False,"message": "domain already exists"}
			return json.dumps(ret)

		else:
				
			url = app.config["ERLANG_SERVER"] +"auth/add-domain/"
			data = urllib.parse.urlencode(mydict)
			headers = {
				'content-type': "application/x-www-form-urlencoded",
				'cache-control': "no-cache",
				}
			#return_value = "success"
			response = requests.request("POST", url, headers=headers, data=data)
			return_value = json.loads(response.text)
			if "error" in return_value.keys():
				ret = {"success": False, "message": return_value["error"]}
				return json.dumps(ret)
			else:			
				ret = {"success": True, "domain_data": return_value}
				return json.dumps(ret)

		
		
	except Exception as e:
		ret = {"success":False,"message":str(e)}
		return json.dumps(ret)



# Email Existence
@app.route('/is-email-registered/<email>',methods = ['GET'])
def email_exists(email):    
		
		print(g.user["username"])
		exists = check_email_existence(email)
		if exists == "true":
			ret = {"success": True, "message": "email already exists"}
			return json.dumps(ret)
		else:
			ret = {"success":False, "message": "email does not exist"}
			return json.dumps(ret)


# Email Verified
@app.route('/is-email-verified/<email>',methods = ['GET'])
@auth_token.token_required
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
@auth_token.token_required
def domain_exists(domain):    
	
		exists = check_domain_existence(domain)

		if exists == "true":
			ret = {"success": True,"message": "domain already exists"}
			return json.dumps(ret)
		else:
			ret = {"success": False,"message": "domain does not exist"}
			return json.dumps(ret)



# Secret Code for Email Verification
@app.route('/verification-code/<email>',methods = ['GET'])
@auth_token.token_required
def verification_code(email):

		print (verification_code)


		url = app.config["ERLANG_SERVER"] +"auth/generate-email-verification-code/" + email
		print (url)
		data = {}
		data = json.dumps(data)
		headers = {}		
		response = requests.request("GET", url, headers=headers, params=data)
		return_value = response.text
		print(return_value)
		# Send email here
		ret = {"success": True, "message": "Verification code has been sent to your registered email"}
		return json.dumps(ret)
		
		 
		 
# Email Verification
@app.route('/verify-email',methods = ["POST"])
@auth_token.token_required
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


	









