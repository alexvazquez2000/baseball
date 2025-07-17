
from flask import Blueprint, render_template, request, redirect, url_for, session
import google_auth_oauthlib.flow
import json
import requests
import facebook
import os
from functools import wraps

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# OAuth configuration
try:
    oauth_config = json.loads(os.environ.get('GOOGLE_OAUTH_SECRETS', '{}'))
    if oauth_config:
        oauth_flow = google_auth_oauthlib.flow.Flow.from_client_config(
            oauth_config,
            scopes=[
                "https://www.googleapis.com/auth/userinfo.email",
                "openid", 
                "https://www.googleapis.com/auth/userinfo.profile",
            ]
        )
except Exception as e:
    print(f"OAuth configuration error: {e}")
    oauth_flow = None

# Facebook OAuth configuration
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_info(access_token):
    return None

# Get user info from Google
def get_google_user_info(access_token):
    response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={
       "Authorization": f"Bearer {access_token}"
    })
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch google user info: {response.status_code} {response.text}")
        return None

# Get user info from Facebook
def get_facebook_user_info(access_token):
    try:
        graph = facebook.GraphAPI(access_token=access_token)
        user_info = graph.get_object('me', fields='id,name,email,picture')
        return user_info
    except Exception as e:
        print(f"Failed to fetch Facebook user info: {e}")
        return None

@auth_bp.route('/login')
def login_page():
    return render_template('login.html')

@auth_bp.route('/login/google')
def google_login():
    if oauth_flow is None:
        return "OAuth not configured. Please set GOOGLE_OAUTH_SECRETS environment variable.", 500

    oauth_flow.redirect_uri = url_for('auth.oauth2callback', _external=True).replace('http://', 'https://')
    authorization_url, state = oauth_flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@auth_bp.route('/login/facebook')
def facebook_login():
    if not FACEBOOK_APP_ID or not FACEBOOK_APP_SECRET:
        return "Facebook OAuth not configured. Please set FACEBOOK_APP_ID and FACEBOOK_APP_SECRET environment variables.", 500
    
    redirect_uri = url_for('auth.facebook_callback', _external=True).replace('http://', 'https://')
    facebook_auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&scope=email"
    return redirect(facebook_auth_url)

@auth_bp.route('/oauth2callback')
def oauth2callback():
    if oauth_flow is None:
        return "OAuth not configured.", 500
    
    if not session.get('state') == request.args.get('state'):
        return 'Invalid state parameter', 400
    
    oauth_flow.fetch_token(authorization_response=request.url.replace('http:', 'https:'))
    session['access_token'] = oauth_flow.credentials.token
    session['auth_provider'] = 'google'
    return redirect("/")

@auth_bp.route('/facebook/callback')
def facebook_callback():
    code = request.args.get('code')
    if not code:
        return 'Authorization failed', 400
    
    redirect_uri = url_for('auth.facebook_callback', _external=True).replace('http://', 'https://')
    token_url = f"https://graph.facebook.com/v18.0/oauth/access_token?client_id={FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&client_secret={FACEBOOK_APP_SECRET}&code={code}"
    
    response = requests.get(token_url)
    if response.status_code == 200:
        token_data = response.json()
        session['access_token'] = token_data['access_token']
        session['auth_provider'] = 'facebook'
        return redirect("/")
    else:
        return 'Failed to get Facebook access token', 400

@auth_bp.route('/logout')
def logout():
    # Revoke tokens based on provider
    if 'access_token' in session:
        access_token = session['access_token']
        auth_provider = session.get('auth_provider', 'google')
        
        if auth_provider == 'facebook' and FACEBOOK_APP_ID and FACEBOOK_APP_SECRET:
            # Revoke Facebook token
            revoke_url = f'https://graph.facebook.com/me/permissions?access_token={access_token}'
            requests.delete(revoke_url)
        elif auth_provider == 'google':
            # Revoke Google token
            revoke_url = f'https://oauth2.googleapis.com/revoke?token={access_token}'
            requests.post(revoke_url, headers={'content-type': 'application/x-www-form-urlencoded'})
    
    session.clear()
    return redirect(url_for('auth.login_page'))
