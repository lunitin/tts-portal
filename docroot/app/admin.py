""" admin.py

Flask routes that require the administrator role

"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, logout_user
from functools import wraps
from . import db, strings
from .models import User, Coverage, Signal, Region, access_table
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
        new_user = User(id = None,
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
    users = User.query.filter(User.security_level == 0).all()

    #Coverage query results with number of signals associated with them. 
    coverages = Coverage.query.all()
    #Coverage.query.join(Signal, Coverage.coverage_id == Signal.coverage_id, isouter = True).with_entities(Coverage.coverage_id, Coverage.coverage_name, func.count(distinct(Signal.signal_number)).label("numSignals")).all()
    
    #Regions 
    regions = Region.query.filter(Region.coverage_id == None)
    return render_template('coverageMgmt.html', userdata = users, coveragedata = coverages, regionData = regions)


"""
Authenticated Coverage Details Page
"""
@admin.route('/coverage-management/<int:coverage_id>', methods=['GET'])
@login_required
@admin_required
def coverage(coverage_id):
    #Grab coverage based on id. 
    coverage = Coverage.query.filter(Coverage.id == coverage_id)

    #Get regions associated with coverage
    regions = Region.query.filter(Region.coverage_id == coverage_id)

    #Get all users that have access to coverage area. 
    users = User.query.filter(User.coverages.any(id = coverage_id))

    return render_template('coverage.html', coveragedata = coverage, regionData = regions, accessdata = users)

"""
Authenticated Coverage Region Page
"""
@admin.route('/coverage-management/<int:coverage_id>/region/<int:region_id>', methods=['GET'])
@login_required
@admin_required
def region(coverage_id,region_id):
    #Grab coverage based on id. 
    regions = Region.query.filter(Region.id == region_id)

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
    #Selected users to add to coverage
    multi_select = request.form.getlist('selectUserList')
    #selected coverage to add users to
    coverage_select_id = request.form.getlist('selectCoverageId')

    coverage = Coverage.query.get(coverage_select_id[0])

    #loop to add each user to coverage. 
    for selected_user in multi_select:
        user = User.query.get(selected_user)
        new_access = User.add_coverages(user,coverage_select_id)
        if (new_access == 0):
            flash("User(s) were successfully added to " + coverage.coverage_name, 'success')
            db.session.commit()
        else:
            flash(selected_user + " was not added to " + coverage.coverage_name, 'danger')
            
    return redirect(url_for('admin.coverages'))

"""
Delete User From Coverage. 
"""
@admin.route('/delete-access/<int:coverage_id>/<int:user_id>')
@login_required
@admin_required
def delete_access(coverage_id, user_id):
    #Selected user to remove from coverage
    selected_user = User.query.get(user_id)
    coverage = Coverage.query.get(coverage_id)
    result = User.remove_coverages(selected_user, [str(coverage_id)])
    if(result == 0):
        flash(selected_user.first_name + "'s access was removed from" + coverage.coverage_name, 'success')        
        db.session.commit()
    else :
        flash(selected_user.first_name + "'s access was not removed from" + coverage.coverage_name, 'danger')        
    return redirect(url_for('admin.coverage', coverage_id=coverage_id))

"""
Add New Coverage. 
"""
@admin.route('/coverage-create', methods=['POST'])
@login_required
@admin_required
def create_coverage():
    create_coverage_name = request.form.get('create_coverage_name')
    multi_select_region = request.form.getlist('add_region')
    error = None

    new_coverage = Coverage(id = None, coverage_name = create_coverage_name)
    db.session.add(new_coverage)
    db.session.commit()  

    for selected_region in multi_select_region:
        region = Region.query.get(selected_region)
        #set region coverage id.  
        region.coverage_id = new_coverage.id
        db.session.commit()  

    flash(create_coverage_name + " was successfully added!", 'success')
    return redirect(url_for('admin.coverages'))


"""
Delete Coverage. 
"""
@admin.route('/coverage-delete/<int:coverage_id>', methods=['POST'])
@login_required
@admin_required
def delete_coverage(coverage_id):
    coverage_delete = Coverage.query.get(coverage_id)
    #Null regions with coverage_id that is being deleted. 
    Region.query.filter(Region.coverage_id == coverage_delete.id).update({Region.coverage_id: None})
    db.session.delete(coverage_delete)
    db.session.commit()

    flash("Coverage deleted Successfully", 'success')
    return redirect(url_for('admin.coverages'))


"""
Remove Region From Coverage. 
"""
@admin.route('/region-remove/<int:region_id>/<int:coverage_id>')
@login_required
@admin_required
def remove_region(region_id, coverage_id):
    remove_region = Region.query.get(region_id)
    #Null regions with coverage_id that is being deleted. 
    remove_region.coverage_id = None
    db.session.commit()

    flash("Region removed Successfully", 'success')
    return redirect(url_for('admin.coverage', coverage_id=coverage_id))

"""
Add Region to Coverage. 
"""
@admin.route('/coverage-add-region', methods=['POST'])
@login_required
@admin_required
def add_region():
    #Query Coverage and Region to add. 
    multi_select_region = request.form.getlist('selectRegionAdd')
    coverage_select_id = request.form.get('selectCoverageRegionAdd')
    coverage = Coverage.query.get(coverage_select_id)
    
    if coverage:
        for region_id in multi_select_region:
            region = Region.query.get(region_id)
            #Set region coverage id to add.  
            region.coverage_id = coverage.id
            db.session.commit()
            flash("Region Added to " + coverage.coverage_name + " Successfully", 'success')
    else:
        flash("Error adding region to " + coverage.coverage_name, 'danger')
    
    return redirect(url_for('admin.coverages'))

"""
Add Region
"""
@admin.route('/region-add', methods=['POST'])
@login_required
@admin_required
def create_region(region_id):
    create_region_name = request.form.get('region_name')

    new_region = Region(id = None,
                        region_name = create_region_name,
                        coverage_id = None)
    db.session.add(new_region)
    db.session.commit()

    flash("Region created Successfully", 'success')
    return redirect(url_for('admin.coverages'))

"""
Remove Region
"""
@admin.route('/region-delete/<int:region_id>', methods=['POST'])
@login_required
@admin_required
def delete_region(region_id):
    delete_region = Region.query.get(region_id)
    db.session.delete(delete_region)
    db.session.commit()

    flash("Region deleted Successfully", 'success')
    return redirect(url_for('admin.coverages'))

# """
# Add Signal to Region
# """
# @admin.route('/signal-add/<int:region_id>', methods=['POST'])
# @login_required
# @admin_required
# def add_region_signal(region_id):
#     