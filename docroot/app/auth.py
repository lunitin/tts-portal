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

"""
description: create new region, and get list of all regions
req:
response:
error:
"""
@auth.route('/region', methods = ['POST', 'GET'])
@login_required
def POST_GET_region(body=None):
   
    return 

"""
description: create new signal, and get list of all signals
req:
response:
error:
"""
@auth.route('/signals', methods = ['POST', 'GET'])
@login_required
def POST_GET_signals(body=None):
    
    return


"""
description: delete, get and update regions with id
req:
response:
error:
"""
@auth.route('/region/<id>', methods = ['DELETE', 'GET', 'PUT'])
@login_required
def DELETE_GET_PUT_region(id):
    
    return 

"""
description: delete, update, and get individual vehicles with id
req:
response:
error:
"""
@auth.route('/vehicles/<id>', methods = ['DELETE', 'GET', 'PUT'])
@login_required
def DELETE_GET_PUT_vehicles(id):
    
    return

"""
description: get and post vehicles. GET all parameters are optional,
    will return all vehicle data that fits the given criteria. Post requires
    all parameters
req:
response:
error:
"""
@auth.route('/vehicles', methods = ['GET', 'POST'])
@login_required
def GET_POST_vehicles(entry_time=None, exit_time=None, travel_direction=None, approach_direction=None, day=None, signal_id=None, stops=None, uturn=None, delay_minimum=None, delay_maximum=None, red_arrival=None, ett_minimum=None, ett_maximum=None, travel_time_minimum=None, travel_time_maximum=None, exit_status=None):  # noqa: E501
    
    return

"""
description: delete, get, and update signals with id
req:
response:
error:
"""
@auth.route('/signals/<id>')
@login_required
def DELETE_GET_PUT_signal_id(id):
    
    return

"""
description: get all vehicle data from single region
req:
response:
error:
"""
@auth.route('/vehicles/region/<id>')
@login_required
def GET_vehicles_from_region(id):
    
    return


"""
description: get all vehicle data from single signal
req:
response:
error:
"""
@auth.route('/vehicles/signal/<id>')
@login_required
def GET_vehicles_from_signal(id):
    
    return

"""
description: delete, get, and update user information with username
req:
response:
error:
"""
@auth.route('/user/<username>')
@login_required
def GET_vehicles_from_signal(username):
    
    return

"""
description: get entire list of users, and create new user
req:
response:
error:
"""
@auth.route('/user)
@login_required
def POST_GET_user():
    
    return