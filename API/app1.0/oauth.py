from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session
import requests
import json, urllib.request, pickle


'''
def send_simple_message(to_email):
    return requests.post(
        "https://api.mailgun.net/v3/stage.clipse.ai/messages",
        #"https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
        auth=("api", "key-ab3c394b8f5f60bc26dcc1c01673f096"),
        data={"from": "Clipse <postmaster@stage.clipse.ai>",
              "to": to_email,
              "subject": "Hello Test",
              "text": "Welcome to Clipse.Congratulations."})
'''   
    


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        

        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=json.loads
        )
        print ("dir(oauth_session)")
        self.access_token = oauth_session.access_token
        session["facebook_token"] = oauth_session.access_token
        
        me = oauth_session.get('/me?fields=id,email,name,picture').json()
        session["facebook_id"] = me["id"]
        
        print ("checkkkkkkkkkkkkkkkkk")
        print (session)
        print (me.get('email'))
        #ret = send_simple_message(me.get('email'))
        print ("ret")
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],  # Facebook does not provide
                                            # username, so the email's user
                                            # is used instead
            me.get('email')
        )







class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        googleinfo = urllib.request.urlopen('https://accounts.google.com/.well-known/openid-configuration')
        google_params = json.load(googleinfo)
        self.service = OAuth2Service(
            name='Google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=google_params.get('authorization_endpoint'),
            access_token_url=google_params.get('token_endpoint'),
            base_url=google_params.get('userinfo_endpoint')
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )
    
    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()
                     },
                decoder = json.loads
        )
        me = oauth_session.get('').json()
        print ("hhhhhhhhhhhhhh")
        return (me['email'], me['name'],
                me['email'])


class LinkedinSignIn(OAuthSignIn):
    def __init__(self):
        super(LinkedinSignIn, self).__init__('linkedin')
        '''
        self.service = OAuth2Service(
            name='linkedin',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
            access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
            base_url='https://api.linkedin.com/v1/'
        )
        '''
        #print self.consumer_id
        #print self.consumer_secret
        self.service = OAuth2Service(
            name='linkedin',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            
            authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
            access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
            base_url='https://api.linkedin.com/v1/'
        )
        '''
        self.service = OAuth1Service(
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            name='linkedin',
            request_token_url='https://api.linkedin.com/uas/oauth/requestToken',
            authorize_url='https://api.linkedin.com/uas/oauth/authorize',
            access_token_url='https://api.linkedin.com/uas/oauth/accessToken',
            base_url='http://api.linkedin.com/v1/')
        '''

    def authorize(self):
        val = self.service.get_authorize_url() 
        print ("lkjhgfdfcg")
        print (val)
        return redirect(self.service.get_authorize_url(
            #scope='r_basicprofile r_emailaddress',
            scope='r_emailaddress',
            response_type='code',
            state='Dgjnfmvosjvomvwhj786768',
            redirect_uri=self.get_callback_url())
            )
        


    '''
    def authorize(self):
        
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()
                     },
                decoder = json.loads
        )
        print "f,mbnfjvnfkvkdfgjv"
        request_token, request_token_secret = self.service.get_request_token()

        session['request_token'] = request_token
        session['request_token_secret'] = request_token_secret
        
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )
        
        return redirect(self.service.get_authorize_url(request_token))
    '''

    def callback(self):       
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()
                     },
                decoder = json.loads
        )

        r = oauth_session.get('/v1/people/~:(id,first-name,last-name,industry,emailAddress)?format=json')
        #r = oauth_session.get('/v1/people/~:(id,first-name,industry,emailAddress)?format=json')
        #r = session.get('people/~/network/updates',
               # params={'type': 'SHAR', 'format': 'json'},
               # header_auth=True)
        updates = r.json()
        print (updates)
        #print "nbvcbm"
        #print updates
        #print type(updates)
    


        return ("okoko","lkjhgh","jhs")



    





