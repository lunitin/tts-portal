""" admin.py

Flask routes that require the administrator role

"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, logout_user
from functools import wraps
from . import strings

admin = Blueprint('admin', __name__)

"""
Decorator to check if the current user is an admin
"""
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash(strings.ERROR_PAGE_PERMISSION_DENIED, "warning")
            return redirect(url_for('auth.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


"""
Test Admin Page
"""
@admin.route('/admin')
@login_required
@admin_required
def test_admin():
    print(current_user.security_level)
    return 'This is an admin only page'
