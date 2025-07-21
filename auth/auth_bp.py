
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from flask_login import  login_user, current_user, logout_user, login_required
#use '.forms' to read from forms.py in the current folder.  If it was in a deeper folder then use ..forms
from .forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm)
import google_auth_oauthlib.flow
import json
import requests
import facebook
import os
from functools import wraps
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_mail import Message
from models import db, Users

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

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.passwd, form.password.data):
            login_user(user, remember=form.remember.data)
            #TODO: validate that next page is valid.
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('welcome'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

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

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data).decode('utf-8')
        user = Users(email=form.email.data, passwd=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

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
        else:
            #it is a flask_login
            logout_user()
    
    session.clear()
    return redirect(url_for('auth.login_page'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    #mail.send(msg)


@auth_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login_page'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@auth_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Users.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data).decode('utf-8')
        user.passwd = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login_page'))
    return render_template('reset_token.html', title='Reset Password', form=form)
