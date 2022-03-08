""" auth.py

Flask routes that require authentication

"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, logout_user
from .Dashboard.dashboard import base_url as dash_url

auth = Blueprint('auth', __name__)


"""
Authenticated Dashboard
"""
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
