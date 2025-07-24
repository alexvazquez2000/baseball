from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response, session
from datetime import datetime
from play_ball.config import Config
from play_ball.models import db, Users, Players, Parents, Coaches, Teams, Seasons, Levels
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required
from flask_mail import Mail
from decimal import Decimal

from play_ball.extension import get_current_season


bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'
login_manager.login_message_category = 'info'
mail = Mail()

  
app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)
#login_manager.user_loader is in auth_bp.py
login_manager.init_app(app)
mail.init_app(app)

#csrf is being used only on the ajax calls
csrf = CSRFProtect(app)

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

#Local imports
from play_ball.api.api_bp import api_bp
from play_ball.auth.auth_bp import auth_bp
from play_ball.coaches.coaches_bp import coaches_bp
from play_ball.ledger.ledger_bp import ledger_bp
from play_ball.parents.parents_bp import parents_bp
from play_ball.players.players_bp import players_bp
from play_ball.reports.reports import reports_bp
from play_ball.seasons.seasons_bp import seasons_bp

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



##To create DB
#with app.app_context():
#    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    #return Users.query.get(int(user_id))
    #This is the only query using the new select style
    return db.session.scalars(db.select(Users).where(Users.id == int(user_id))).first()

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


