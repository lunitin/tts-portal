""" admin.py

Flask routes that require the administrator role

"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, logout_user
from functools import wraps
from . import db, strings
from .models import User, Access, Coverage, Signal, Region
from sqlalchemy import func, distinct
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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


"""
Authenticated User Management Page
"""
@admin.route('/user-management', methods=['GET'])
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('users.html', userdata = users)


"""
Create new user.
"""
@admin.route('/create-user', methods=['POST'])
@login_required
@admin_required
def create_user():
    form_fname = request.form.get('first_name')
    form_lname = request.form.get('last_name')
    form_email = request.form.get('email_address')
    form_security = request.form.get('security_level')
    form_password = request.form.get('password')
    error = None

    if not form_fname or not form_fname.strip():
        error = 'First name is missing'
    if not form_lname or not form_lname.strip():
        error = 'First name is missing'
    if not form_email or not form_email.strip() or '@' not in form_email:
        error = 'Email is missing or needs "@"'
    if not form_password or not form_password.strip():
        error = 'Password is required'

    if error:
        flash(error, 'warning')
        return redirect(url_for('auth.users'))

    existing_email = User.query.filter(User.email_address == form_email).one_or_none()

    if existing_email is None:
        new_user = User(user_id = None,
                        first_name = form_fname,
                        last_name = form_lname,
                        email_address = form_email,
                        security_level = form_security,
                        password = generate_password_hash(form_password,method='pbkdf2:sha256:310000', salt_length=128),
                        date_created = datetime.now(),
                        date_last_password_change = datetime.now()
                        )

        #Add to db
        db.session.add(new_user)
        db.session.commit()
        flash("Account " + form_email + " was created!", 'success')
        return redirect(url_for('admin.users'))

    else:
        flash("Account with" + form_email + " already exists", 'danger')
        return redirect(url_for('admin.users'))

"""
Update user.
"""
@admin.route('/update/<int:user_id>',  methods = ['POST'])
@login_required
@admin_required
def update(user_id):
    user_update = User.query.get(user_id)
    user_update.first_name = request.form.get('first_name')
    user_update.last_name = request.form.get('last_name')
    user_update.email_address = request.form.get('email_address')
    user_update.security_level = request.form.get('security_level')
    db.session.commit()

    flash("User " + user_update.first_name + ", " + user_update.last_name + " Updated Successfully!", 'success')
    return redirect(url_for('admin.users'))


@admin.route('/delete/<int:user_id>',  methods = ['POST'])
@login_required
@admin_required
def delete(user_id):
    user_delete = User.query.get(user_id)
    db.session.delete(user_delete)
    db.session.commit()

    flash("User deleted Successfully", 'success')
    return redirect(url_for('admin.users'))


"""
Authenticated Coverage Management Page
"""
@admin.route('/coverage-management', methods=['GET'])
@login_required
@admin_required
def coverages():
    users = User.query.all()

    #Coverage query results with number of signals associated with them.
    coverages = Coverage.query.all()
    #Coverage.query.join(Signal, Coverage.coverage_id == Signal.coverage_id, isouter = True).with_entities(Coverage.coverage_id, Coverage.coverage_name, func.count(distinct(Signal.signal_number)).label("numSignals")).all()

    #Regions
    regions = Region.query.all()
    return render_template('coverageMgmt.html', userdata = users, coveragedata = coverages, regionData = regions)


"""
Authenticated Coverage Details Page
"""
@admin.route('/coverage-management/<int:coverage_id>', methods=['GET'])
@login_required
@admin_required
def coverage(coverage_id):
    #Grab coverage based on id.
    coverage = Coverage.query.filter(Coverage.coverage_id == coverage_id)

    #Get signals associated with coverage
    regions = Region.query.filter(Region.coverage_id == coverage_id)

    #Get all users that have access to coverage area.
    accesses = User.query.join(Access).where(Access.coverage_id == coverage_id).all()
    return render_template('coverage.html', coveragedata = coverage, accessdata = accesses, regionData = regions)

"""
Authenticated Coverage Details Page
"""
@admin.route('/coverage-management/<int:coverage_id>/region/<int:region_id>', methods=['GET'])
@login_required
@admin_required
def region(coverage_id,region_id):
    #Grab coverage based on id.
    regions = Region.query.filter(Region.region_id == region_id)

    #Get signals associated with coverage
    signals = Signal.query.filter(Signal.region_id == region_id)

    return render_template('region.html', regionData = regions, signalData = signals)


"""
Add User(s) to Coverage.
"""
@admin.route('/coverage-add', methods=['POST'])
@login_required
@admin_required
def add_coverage():
    multi_select = request.form.getlist('selectUserList')
    coverage_select_id = request.form.get('selectCoverageId')
    error = None

    coverage = Coverage.query.get(coverage_select_id)

    for user_id in multi_select:
        user = User.query.get(user_id)
        new_access = Access(access_id = None, user_id = user.user_id, coverage_id = coverage.coverage_id)
        db.session.add(new_access)

    db.session.commit()

    flash("Users were successfully added to " + coverage.coverage_name, 'success')
    return redirect(url_for('admin.coverages'))

"""
Add New Coverage. 
"""
@admin.route('/coverage-create', methods=['POST'])
@login_required
@admin_required
def create_coverage():
    multi_select_signals = request.form.getlist('add_signal')
    coverage_select_name = request.form.get('create_coverage_name')
    error = None

    # valid_coverage = Coverage.query.filter(Coverage.coverage_name = coverage_select_name)

    new_coverage = Coverage(coverage_id = None, coverage_name = coverage_select_name)
    db.session.add(new_coverage)

    # for user_id in multi_select:
    #     user = User.query.get(user_id)
    #     new_access = Access(access_id = None, user_id = user.user_id, coverage_id = coverage.coverage_id)
    #     db.session.add(new_access)

    db.session.commit()

    flash(coverage_select_name + " was successfully added!", 'success')
    return redirect(url_for('admin.coverages'))
