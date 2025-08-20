
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from flask_login import  login_user, current_user, logout_user, login_required
#use '.forms' to read from forms.py in the current folder.  If it was in a deeper folder then use ..forms
from .forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm)
import json
import requests
import os
from functools import wraps
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_mail import Message
from play_ball.models import db, Users
from play_ball.app import mail

#using flash-login to track the current user https://flask-login.readthedocs.io/en/latest/#flask_login.current_user
auth_bp = Blueprint('auth', __name__, template_folder='templates')

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
        #TODO: instead take them to a page to enter parent and player information
        return redirect(url_for('auth.login_page'))
    return render_template('register.html', title='Register', form=form)

@auth_bp.route('/logout')
def logout():
    #log them out with flask_login
    #this includes session.clear() - don't run clear() again or the remember me option doesn't behave correctly
    logout_user()
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
    #FIXME: Emails are not working because omnis. ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it   
    mail.send(msg)


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
