import sys
sys.path.append("/usr/local/bin/newflask/lib/python3.6/site-packages")   # comment this when push to GIT

from flask import Flask
from flask import g,Flask, redirect, url_for, render_template, flash, json, render_template_string
from flask import request, redirect, session, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user






from flask import g, Flask


app = Flask(__name__)
app.config.from_object('config')

ctx= app.app_context()
ctx.push()
g._app = ctx


from .controllers import auth, sociallogin, emails, users, events


lm = LoginManager(app)     #For social login



if __name__ == "__main__":
    app.run()
