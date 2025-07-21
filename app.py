from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response, session
from datetime import datetime
from config import Config
from models import db, Users, Players, Parents, Coaches, Teams, Seasons, Levels
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required
from flask_mail import Mail

#Local imports
from decimal import Decimal
from api.api_bp import api_bp
from auth.auth_bp import auth_bp
from coaches.coaches_bp import coaches_bp
from ledger.ledger_bp import ledger_bp
from parents.parents_bp import parents_bp
from players.players_bp import players_bp
from reports.reports import reports_bp
from seasons.seasons_bp import seasons_bp
from extension import get_current_season

app = Flask(__name__)

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#login_manager.user_loader is in auth_bp.py
login_manager.init_app(app)

#app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
#app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

app.config['MAIL_SERVER'] = 'mail.guardedhost.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(coaches_bp, url_prefix='/coaches')
app.register_blueprint(ledger_bp, url_prefix='/ledger')
app.register_blueprint(parents_bp, url_prefix='/parents')
app.register_blueprint(players_bp, url_prefix='/players')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(seasons_bp, url_prefix='/seasons')


#To record all SQL Queries enable SQLALCHEMY_ECHO
#app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

#csrf is being used only on the ajax calls
csrf = CSRFProtect(app)

##To create DB
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

def inject_current_year():
    (current_season_id, current_season_name) = get_current_season()
    return {'current_year': datetime.now().year,
      'current_season_name': current_season_name,
      'current_season_id': current_season_id,
       }

app.context_processor(inject_current_year)

# -- Welcome page: show teams in current season (e.g. "2025") --
@app.route('/')
@app.route('/home')
@login_required
def welcome():
    user_info = None
    #print (session.get('auth_provider'))
    (current_season_id, current_season_name) = get_current_season()
    teams = Teams.query.filter_by(season_id=current_season_id).all()
    return render_template('welcome.html', teams=teams, user_info=user_info)


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
