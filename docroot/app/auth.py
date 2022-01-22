from flask import Blueprint, redirect
from flask_login import login_required, current_user, logout_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/contact')
@login_required
def contact_us():
    print(current_user, flush=True)
    return 'Contact US'

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('anon.index'))
