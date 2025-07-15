from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response, session
from datetime import datetime
from config import Config
from models import db, Players, Parents, Coaches, Teams, Seasons, Levels
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import google_auth_oauthlib.flow
import json
import requests
from functools import wraps
import facebook

#Local imports
from decimal import Decimal
from api.api_bp import api_bp
from coaches.coaches_bp import coaches_bp
from ledger.ledger_bp import ledger_bp
from parents.parents_bp import parents_bp
from players.players_bp import players_bp
from reports.reports import reports_bp
from seasons.seasons_bp import seasons_bp
from extension import get_current_season

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(coaches_bp, url_prefix='/coaches')
app.register_blueprint(ledger_bp, url_prefix='/ledger')
app.register_blueprint(parents_bp, url_prefix='/parents')
app.register_blueprint(players_bp, url_prefix='/players')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(seasons_bp, url_prefix='/seasons')

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads'

#To record all SQL Queries enable SQLALCHEMY_ECHO
#app.config['SQLALCHEMY_ECHO'] = True

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

#csrf is being used only on the ajax calls
csrf = CSRFProtect(app)

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

##To create DB
with app.app_context():
    db.create_all()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #if 'access_token' not in session:
        #    return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# Get user info from Google
def get_user_info(access_token):
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

def inject_current_year():
    (current_season_id, current_season_name) = get_current_season()
    return {'current_year': datetime.now().year,
      'current_season_name': current_season_name,
      'current_season_id': current_season_id,
       }

app.context_processor(inject_current_year)

# -- Welcome page: show teams in current season (e.g. "2025") --
@app.route('/')
@login_required
def welcome():
    user_info = None
    if 'access_token' in session:
        if session.get('auth_provider') == 'facebook':
            user_info = get_facebook_user_info(session['access_token'])
        else:
            user_info = get_user_info(session['access_token'])
    (current_season_id, current_season_name) = get_current_season()
    teams = Teams.query.filter_by(season_id=current_season_id).all()
    return render_template('welcome.html', teams=teams, user_info=user_info)

# -- Authentication Routes --
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login/google')
def google_login():
    if oauth_flow is None:
        return "OAuth not configured. Please set GOOGLE_OAUTH_SECRETS environment variable.", 500

    oauth_flow.redirect_uri = url_for('oauth2callback', _external=True).replace('http://', 'https://')
    authorization_url, state = oauth_flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/login/facebook')
def facebook_login():
    if not FACEBOOK_APP_ID or not FACEBOOK_APP_SECRET:
        return "Facebook OAuth not configured. Please set FACEBOOK_APP_ID and FACEBOOK_APP_SECRET environment variables.", 500
    
    redirect_uri = url_for('facebook_callback', _external=True).replace('http://', 'https://')
    facebook_auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&scope=email"
    return redirect(facebook_auth_url)

@app.route('/oauth2callback')
def oauth2callback():
    if oauth_flow is None:
        return "OAuth not configured.", 500
    
    if not session.get('state') == request.args.get('state'):
        return 'Invalid state parameter', 400
    
    oauth_flow.fetch_token(authorization_response=request.url.replace('http:', 'https:'))
    session['access_token'] = oauth_flow.credentials.token
    session['auth_provider'] = 'google'
    return redirect("/")

@app.route('/facebook/callback')
def facebook_callback():
    code = request.args.get('code')
    if not code:
        return 'Authorization failed', 400
    
    redirect_uri = url_for('facebook_callback', _external=True).replace('http://', 'https://')
    token_url = f"https://graph.facebook.com/v18.0/oauth/access_token?client_id={FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&client_secret={FACEBOOK_APP_SECRET}&code={code}"
    
    response = requests.get(token_url)
    if response.status_code == 200:
        token_data = response.json()
        session['access_token'] = token_data['access_token']
        session['auth_provider'] = 'facebook'
        return redirect("/")
    else:
        return 'Failed to get Facebook access token', 400

@app.route('/logout')
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
    return redirect(url_for('login_page'))


# -- Extra navigation links on welcome page --

@app.route('/parents_page')
def parents_page():
    return redirect(url_for('parents.list_parents'))

@app.route('/teams_page')
def teams_page():
    return redirect(url_for('seasons.list_teams'))

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    photo = request.files['photo']
    filename = secure_filename(f"{str(int.from_bytes(os.urandom(6), 'big'))}.jpg")
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    photo.save(path)
    return filename

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True,ssl_context='adhoc')
    app.run(host='0.0.0.0', debug=True)
    #app.run()
