
from flask import g,Flask, redirect, url_for, render_template, flash, json, render_template_string
from flask import request, redirect, session, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
#from flask_login import LoginManager, UserMixin, login_user, logout_user
import flask
import requests
from  oauth import OAuthSignIn

#from flask import logout_user

val= getattr(g,'_app',None)

app = val.app




@app.route('/logout')
def logout():
    logout_user()
    if ('credentials') in flask.session:
    #if flask.session.has_key('credentials'):
        flask.session.pop('credentials')
    ret = {"status":200, "message": "User logged out successfully"}
    return json.dumps(ret)




