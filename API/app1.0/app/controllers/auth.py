
from flask import g,Flask, redirect, url_for, render_template, flash, json, render_template_string
from flask import request, redirect, session, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
import urllib
import requests
import bcrypt
from  oauth import OAuthSignIn
from . import emails as email_service
from ..helpers import auth_token

from flask import Flask

import json



val= getattr(g,'_app',None)

app = val.app

# Email Signup
@app.route('/signup', methods = ['POST'])
def sign_up():    
    try:

        mydict = json.loads(request.data.decode('utf-8'))

        email = mydict["email"]
        domain = mydict["domain"]

        exists = email_service.check_email_existence(email)

        if exists == "true":

            ret = {"success": False, "message": "email already exists"}
            return json.dumps(ret)

        else:

            url = app.config["ERLANG_SERVER"] +"auth/add-user/"
            data = urllib.parse.urlencode({"email": email, "domain": domain, "is_email_verified": False, "status": "active", "user_agent":str(request.user_agent)})
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache"
                }
            response = requests.request("POST", url, headers=headers, data=data)
            return_value = json.loads(response.text)
            if "error" in return_value.keys():
                ret = {"success": False, "message": return_value["error"]}
                return json.dumps(ret)
            else:
                token = auth_token.tokenize(return_value)           
                ret = {"success":True, "token": token.decode('utf-8')}
                return json.dumps(ret)
    
    except Exception as e:
        ret = {"success":False,"message":str(e)}
        return json.dumps(ret)



@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        ret = {"status":200, "message": "User logged in successfully"}
        return json.dumps(ret)
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/auth/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    data = oauth.callback()
    print (data , provider)
    social_id = data[0]
    username = data[1]
    email = data[2]
    if social_id is None:
        ret = {"status":500, "message": "Authentication failed"}
        return json.dumps(ret)
    

    ret = {"status":200, "message": "User logged in successfully"}
    return json.dumps(ret)



# Secret code for login
@app.route('/login-code/<username>',methods = ['GET'])
def login_code(username):


        url = app.config["ERLANG_SERVER"] +"auth/generate-login-code/" + username
        data = {}
        data = json.dumps(data)
        headers = {}        
        response = requests.request("GET", url, headers=headers, params=data)
        return_value = response.text
        print (response)
        print(return_value)
        # Send email here
        ret = {"success": True, "message": "Login code has been sent to your primary email"}
        return json.dumps(ret)




# Email login
@app.route('/login',methods = ["POST"])
def log_in():    
    try:
        mydict = json.loads(request.data.decode('utf-8'))

        # if "password" in mydict.keys():
        #     password = bcrypt.hashpw(mydict["password"].encode('utf-8', app.config.get('ROUND')), bcrypt.gensalt())
        #     mydict["password"] = password
        
        url = app.config["ERLANG_SERVER"] + "auth/login"
        data = urllib.parse.urlencode(mydict)
        headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache"
                }
        response = requests.request("POST", url, headers=headers, data=data)
        return_value = json.loads(response.text)
        if "error" in return_value.keys():
            ret = {"success":False,"message": return_value["error"]}
            return json.dumps(ret)
        else:
            token = auth_token.tokenize(return_value)
            ret = {"success":True, "token":token.decode('utf-8')}
            return json.dumps(ret)
           
    except Exception as e:
        ret = {"success":False,"message":str(e)}
        return json.dumps(ret)


