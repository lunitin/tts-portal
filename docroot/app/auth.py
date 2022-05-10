""" auth.py

Flask routes that require authentication

"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, logout_user
from . import db, strings
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
    print(current_user, flush=True)
    return render_template('myaccount.html')


"""
Route to request a password change
"""
@auth.route('/change-password', methods=['GET'])
@login_required
def change_password():
    return render_template('changepassword.html')


"""
Change the password for the current user
"""
@auth.route('/change-password', methods=['POST'])
@login_required
def change_password_post():
    old_password = request.form.get('old_password')
    password1 = request.form.get('password')
    password2 = request.form.get('password2')

    # Verify that the two password strings match
    if password1 != password2:
        flash(strings.ERROR_PASSWORD_MISMATCH, 'danger')
        return redirect(url_for('auth.change_password'))

    # Check complexity requirements???

    # Load the user found in the token
    user = User.query.filter_by(id=current_user.id).first()

    # Check if the old password matches
    # check if the user actually exists
    # take old password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, old_password):
        flash(strings.ERROR_PASSWORD_INVALID, 'danger')
        return redirect(url_for('auth.change_password'))

    try:
        user.password = generate_password_hash(password1, method='pbkdf2:sha256:310000', salt_length=128),
        db.session.commit()
        print("=== pass:", user.password)
        flash(strings.MSG_PASSWORD_RESET, 'success')

        logout_user();
        return redirect(url_for('anon.login', next=url_for('auth.dashboard')))
    except BaseException:
        # @TODO Add more robust exception handling
        flash(strings.ERROR_PASSWORD_RESET, 'danger')

    return redirect(url_for('auth.my_account'))


"""
Log out of the current session
"""
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('anon.login', next=url_for('auth.dashboard')))
