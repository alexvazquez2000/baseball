from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response, Response, session
from datetime import datetime
from config import Config
from models import db, Players, Parents, Coaches, Teams, Seasons
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from flask import jsonify
import google_auth_oauthlib.flow
import json
import requests
from functools import wraps
import facebook
#Local imports
from thumbnail import Thumbnail

#for PDF
#from flask import make_response
from fpdf import FPDF

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads'
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
        if 'access_token' not in session:
            return redirect(url_for('login_page'))
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
        print(f"Failed to fetch user info: {response.status_code} {response.text}")
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
    return {'current_year': datetime.now().year}

app.context_processor(inject_current_year)

# -- Welcome page: show teams in current season (e.g. "2025") --
@app.route('/')
@login_required
def welcome():
    #current_season = "2025-Spring"  # or dynamic if you want
    current_season = Seasons.query.limit(1).first()
    teams = Teams.query.filter_by(season=current_season).all()
    #teams = Teams.query.all()
    user_info = None
    if 'access_token' in session:
        if session.get('auth_provider') == 'facebook':
            user_info = get_facebook_user_info(session['access_token'])
        else:
            user_info = get_user_info(session['access_token'])
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
        return 'Failed to get access token', 400

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

# -- Ajax --


# -- Players --
@app.route('/players')
@login_required
def list_players():
    players = Players.query.all()
    return render_template('players.html', players=players)

@app.route('/player', methods=['GET', 'POST'])
@login_required
def edit_player():
    player = {}
    player_id = request.args.get('player_id')
    if request.method == 'POST':
        #get the ID from the post data if present
        player_id = request.form['id'] 
        if player_id:
            #update existing entry
            player = Players.query.get_or_404(player_id)
            player.name = request.form['name']
            player.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            player.jersey_number = int(request.form['jersey_number'])
        else :
            #add new player / player_id is empty
            dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            player = Players(
                name=request.form['name'],
                date_of_birth=dob,
                jersey_number=int(request.form['jersey_number'])
            )
            db.session.add(player)
        db.session.commit()
        return redirect(url_for('list_players'))

    dob = ''
    if player_id :
        player = Players.query.get_or_404(player_id)
        dob = player.date_of_birth.strftime('%Y-%m-%d')
    return render_template('edit_player.html', player=player, dob=dob)


# -- Parents --

@app.route('/parents')
@login_required
def list_parents():
    parents = Parents.query.all()
    return render_template('parents.html', parents=parents)

@app.route('/parent/add', methods=['GET', 'POST'])
@login_required
def add_parent():
    if request.method == 'POST':
        parent = Parents(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone']
        )
        db.session.add(parent)
        db.session.commit()
        return redirect(url_for('list_parents'))
    return render_template('add_parent.html')

@app.route('/parent/<int:parent_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_parent(parent_id):
    parent = Parents.query.get_or_404(parent_id)
    players = Players.query.all()
    if request.method == 'POST':
        parent.name = request.form['name']
        parent.email = request.form['email']
        parent.phone = request.form['phone']
        # Clear current children
        parent.players.clear()
        # Add selected children
        child_ids = request.form.getlist('children')
        for cid in child_ids:
            player = Players.query.get(int(cid))
            if player:
                parent.players.append(player)
        db.session.commit()
        return redirect(url_for('list_parents'))
    return render_template('edit_parent.html', parent=parent, players=players)

#Ajax
@app.route("/parents/search")
def search_parents():
    """Search parents by name, returns JSON."""
    q = request.args.get("q", "")
    results = []
    if q:
        results = Parents.query.filter(Parents.name.ilike(f"%{q}%")).all()
    data = [{"id": p.id, "name": p.name, "phone": p.phone} for p in results]
    return jsonify(data)

@app.route("/player/<int:player_id>/add_parent_ajax", methods=["POST"])
def add_parent_ajax(player_id):
    parent_id = request.json.get("parent_id")
    player = Players.query.get(player_id)
    parent = Parents.query.get(parent_id)

    if parent and player and parent not in player.parents:
        player.parents.append(parent)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

#Ajax
@app.route("/player/<int:player_id>/remove_parent_ajax", methods=["POST"])
def remove_parent_ajax(player_id):
    parent_id = request.json.get("parent_id")
    player = Players.query.get(player_id)
    parent = Parents.query.get(parent_id)

    if parent and player and parent in player.parents:
        player.parents.remove(parent)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

# -- Coaches --

@app.route('/coaches')
@login_required
def list_coaches():
    coaches = Coaches.query.all()
    return render_template('coaches.html', coaches=coaches)

@app.route('/coach', methods=['GET', 'POST'])
@login_required
def edit_coach():
    coach = {}
    coach_id = request.args.get('id')
    if request.method == 'POST':
        # Handle uploaded or captured photo
        photo_data = None
        thumbnail_data = None
        if "photo" in request.files and request.files["photo"].filename:
            photo_data = request.files["photo"].read()
            thumbnail_data = Thumbnail.create_thumbnail(photo_data)

        #get the coach ID from the post data if present
        coach_id = request.form['id'] 
        if coach_id:
            #update existing entry
            coach = Coaches.query.get_or_404(coach_id)
            coach.name = request.form['name']
            coach.email = request.form['email']
            coach.phone = request.form['phone']
            if photo_data:
                # Only overwrite if new photo uploaded
                coach.photo = photo_data
                coach.thumbnail=thumbnail_data
        else :
            #add new coach / coach_id is empty
            coach = Coaches(
                name=request.form['name'],
                email=request.form['email'],
                phone=request.form['phone'],
                photo=photo_data,
                thumbnail=thumbnail_data
            )
            db.session.add(coach)
        db.session.commit()
        return redirect(url_for('list_coaches'))

    if coach_id :
        coach = Coaches.query.get_or_404(coach_id)
    return render_template('edit_coach.html', coach=coach)

@app.route("/photo/<int:coach_id>")
def get_photo(coach_id):
    coach = Coaches.query.get_or_404(coach_id)
    if coach and coach.photo:
        return Response(coach.photo, mimetype="image/jpeg")
    return '', 404

@app.route("/photo/thumbnail/<int:coach_id>")
def get_thumbnail(coach_id):
    coach = Coaches.query.get_or_404(coach_id)
    if coach and coach.thumbnail:
        return Response(coach.thumbnail, mimetype="image/jpeg")
    return '', 404

# -- Seasons --
@app.route('/seasons')
@login_required
def list_seasons():
    seasons = Seasons.query.all()
    return render_template('seasons.html', seasons=seasons)
@app.route('/season/add', methods=['GET', 'POST'])
@login_required
def add_season():  
    if request.method == 'POST':
        season = Seasons(
            name=request.form['name'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        )
        db.session.add(season)
        db.session.commit()
        return redirect(url_for('list_seasons'))
    return render_template('add_season.html')
@app.route('/season/<int:season_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_season(season_id):
    season = Seasons.query.get_or_404(season_id)
    if request.method == 'POST':
        season.name = request.form['name']
        season.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        season.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        db.session.commit()
        return redirect(url_for('list_seasons'))
    return render_template('edit_season.html', season=season)
# -- Create new season --
@app.route('/create_new_season', methods=['GET', 'POST'])
@login_required
def create_new_season():
    if request.method == 'POST':
        # Get the current season
        current_season = Seasons.query.order_by(Seasons.id.desc()).first()
        if current_season:
            # Create a new season based on the current one
            new_season = Seasons(
                name=f"{current_season.name} - New",
                start_date=current_season.start_date,
                end_date=current_season.end_date
            )
            db.session.add(new_season)
            db.session.commit()
            return redirect(url_for('list_seasons'))
    return render_template('create_new_season.html')

# -- Teams --

@app.route('/teams')
@login_required
def list_teams():
    teams = Teams.query.all()
    return render_template('teams.html', teams=teams)

@app.route('/team/add', methods=['GET', 'POST'])
@login_required
def add_team():
    coaches = Coaches.query.all()
    players = Players.query.all()
    if request.method == 'POST':
        team = Teams(
            teamName=request.form['teamName'],
            season=request.form['season'],
        )
        # Add coaches
        coach_ids = request.form.getlist('coaches')
        for cid in coach_ids:
            coach = Coaches.query.get(int(cid))
            if coach:
                team.coaches.append(coach)
        # Add players
        player_ids = request.form.getlist('players')
        for pid in player_ids:
            player = Players.query.get(int(pid))
            if player:
                team.players.append(player)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('list_teams'))
    return render_template('add_team.html', coaches=coaches, players=players)

@app.route('/team/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    team = Teams.query.get_or_404(team_id)
    coaches = Coaches.query.all()
    players = Players.query.all()
    if request.method == 'POST':
        team.teamName = request.form['teamName']
        team.season = request.form['season']
        # Update coaches
        team.coaches.clear()
        coach_ids = request.form.getlist('coaches')
        for cid in coach_ids:
            coach = Coaches.query.get(int(cid))
            if coach:
                team.coaches.append(coach)
        # Update players
        team.players.clear()
        player_ids = request.form.getlist('players')
        for pid in player_ids:
            player = Players.query.get(int(pid))
            if player:
                team.players.append(player)
        db.session.commit()
        return redirect(url_for('list_teams'))
    return render_template('edit_team.html', team=team, coaches=coaches, players=players)


# -- Experimental section
@app.route('/generate-pdf')
def generate_pdf():
	# https://py-pdf.github.io/fpdf2/Tutorial.html#tuto-1-minimal-example
    #Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    # Add content to the PDF
    pdf.cell(200, 10, txt="Hello from Flask and FPDF!", ln=1, align="C")
    pdf.cell(200, 10, txt="This is a dynamically generated PDF.", ln=1, align="C")

    # PDF is ready
    # for usage on flask https://py-pdf.github.io/fpdf2/UsageInWebAPI.html

    # Output the PDF as bytes
    pdf_output = pdf.output(dest='S').encode('latin-1')
    # Create a Flask response and Output the PDF as bytes
    response = make_response(pdf_output)
    # Set appropriate headers for PDF
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=generated_document.pdf" 
    return response

# -- Extra navigation links on welcome page --

@app.route('/parents_page')
def parents_page():
    return redirect(url_for('list_parents'))

@app.route('/teams_page')
def teams_page():
    return redirect(url_for('list_teams'))

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
    app.run(host='0.0.0.0', debug=True,ssl_context='adhoc')
    #app.run(host='0.0.0.0', debug=True)
    #app.run()
