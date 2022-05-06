""" auth.py

Flask routes that require authentication

"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user, logout_user
from . import db
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .Dashboard.dashboard import base_url as dash_url

auth = Blueprint('auth', __name__)


"""
Authenticated Dashboard
"""
@auth.route('/')
@auth.route('/dashboard')
@auth.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html', dash_url = dash_url)


"""
Display information about the account
"""
@auth.route('/my-account')
@login_required
def my_account():
    user = User.query.get(current_user.id)
    if (user.security_level == 0):
        coverages = User.query.get(current_user.id).coverages
        return render_template('myaccount.html', coverages = coverages)
    else: 
        coverages = Coverage.query.all()
        return render_template('myaccount.html', coverages = coverages)


"""
Log out of the current session
"""
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('anon.login', next=url_for('auth.dashboard')))