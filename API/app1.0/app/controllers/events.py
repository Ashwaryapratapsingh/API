from flask import g,Flask, redirect, url_for, render_template, flash, json, render_template_string
from flask import request, redirect, session, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
	current_user
#from flask_login import LoginManager, UserMixin, login_user, logout_user
import flask
import requests
import json
import urllib	
import urllib.request



from datetime import datetime
import icalendar
from icalendar import Calendar, Event, vDatetime
import glob, os





#from apiclient import discovery
#from oauth2client import client
#from oauth2client import tools
#from oauth2client.file import Storage

from rauth.service import OAuth2Service

#from oauth2client.client import flow_from_clientsecrets
#from oauth2client.client import OAuth2WebServerFlow
#import httplib2
from datetime import datetime





val= getattr(g,'_app',None)

app = val.app





# Facebook events application
@app.route('/facebook/events')
def facebook_events():
    
    url_events = "https://graph.facebook.com/" + session["facebook_id"] + "/events?access_token=" + session["facebook_token"]
    print (url_events)
    val = urllib.request.urlopen(url_events)
    
    
    return json.dumps(str(val.read()))
 	#return json.dumps(val.read())




'''
@app.route('/apple/events')
def apple_events():
	start_format = "%a %b %d %H:%M" #datetime(2017, 6, 1)
	end_format = "%H:%M" #(2017, 6, 31)

def parse_ics(infile):
	
	cal = Calendar.from_ical(infile.read())

	events = []

	for component in cal.walk('vevent'):
		event =   component.get('summary')
		description =  component.get('description')
		location =  component.get('location')
		start = component.get('dtstart')
		end = component.get('dtend')
		total_time =  "%s-%s" % (start.dt.strftime(start_format) , end.dt.strftime(end_format))
		#line =  "Summary:%s \nDescription: %s \nLocation: %s \nTime: %s \n------\n " % (event, description, location, total_time)
		line = {"Summary": summary, "Description": description, "Location":location, "Time":time}
		print (line)

	return events()

def ics_to_file(filename, events):
	with open(filename, 'w') as f:
		for e in events:
			f.write(e.encode('utf-8')) 

		convert_file()

'''



# Facebook friends application
@app.route('/facebook/friends')
def facebook_friends():
    
    url_friends = "https://graph.facebook.com/" + session["facebook_id"] + "/friends?access_token=" + session["facebook_token"]
    print (url_friends)
    val = urllib.request.urlopen(url_friends)
    
    
    return json.dumps(str(val.read()))
 	#return json.dumps(val.read())





