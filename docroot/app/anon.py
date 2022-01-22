from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


anon = Blueprint('anon', __name__)


"""
Default home page route
"""
@anon.route('/')
def index():
    print(current_user, flush=True)
    return render_template('index.html')


"""
Display the login form
"""
@anon.route('/login')
def login():
    return render_template('login.html')


"""
Attempt to log a user in to the system
"""
@anon.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email_address=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')

        return redirect(url_for('anon.login'))

    flash('You are logged in!')
    login_user(user, remember=remember)
    return redirect(url_for('auth.dashboard'))



@anon.route('/forgot-password')
def forgot_password():
    return 'Forgot Password'


@anon.route('/recover-password')
def recover_password():
    return 'Recover Password'




"""
Temporary account creation route to test hash generation
"""
@anon.route('/create-account')
def create_account():
    # code to validate and add user to database goes here
    email_address = 'test2@example.org'
    first_name = 'Static Test'
    last_name = 'Last'
    password = 'test123'
    security_level = 1;


    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email_address=email_address).first()

    # if a user is found, we want to redirect back to signup page so user can try again
    if user:
        flash("Account already exists!")
        return redirect(url_for('anon.login'))

    # create a new user with the form data.
    # Password hash recommendation sizes from:
    # https://en.wikipedia.org/wiki/PBKDF2
    new_user = User(email_address=email_address, first_name=first_name,
            last_name=last_name,
            security_level=1,
            password=generate_password_hash(password, method='pbkdf2:sha256:310000', salt_length=128),
            date_created=datetime.now(),
            date_last_password_change=datetime.now()
            )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    flash("Account" + email_address + " created!")
    return redirect(url_for('anon.login'))
