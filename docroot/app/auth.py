""" auth.py

Flask routes that require authentication

"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, logout_user
from . import db

auth = Blueprint('auth', __name__)

"""
Authenticated Dashboard
"""
@auth.route('/dashboard')
@login_required
def dashboard():
    print(current_user, flush=True)
    return render_template('dashboard.html')

"""
Display information about my account
"""
@auth.route('/my-account')
@login_required
def my_account():
    print(current_user, flush=True)
    return render_template('myaccount.html')

"""
Log out of the current session
"""
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('anon.index'))