""" anon.py
Flask routes that do not require authentication
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import BadSignature, BadData, SignatureExpired
import base64
import smtplib
import json

from . import db, config, strings, mail
from .models import User

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
@anon.route('/login', methods=['GET'])
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
        flash(strings.ERROR_USER_NOT_FOUND_INVALID_PASS, 'warning')
        return redirect(url_for('anon.login'))

    flash(strings.MSG_LOGIN_WELCOME_BACK, 'success')

    login_user(user, remember=remember)

    return redirect(url_for('auth.dashboard'))


"""
Route to request a password change
"""
@anon.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('forgotpassword.html')


"""
Send a forgot password e-mail to the user
"""
@anon.route('/forgot-password', methods=['POST'])
def forgot_password_post():
    template = 'forgotpassword.html'
    email = request.form.get('username')

    # Look up the user
    user = User.query.filter_by(email_address=email).first()

    if not user:
        flash(strings.ERROR_FORGOT_PASSWORD_USER_NOT_FOUND, 'danger')
        return render_template(template)

    # Generate a magic link
    try:
        s1 = Serializer(config.IDS_SECRET_KEYS, salt="forgot-password", expires_in=config.IDS_FORGOT_PASSWORD_VALIDITY_TIMER)
        raw_token = s1.dumps({'id': user.get_id() })

        # Base64 URLEncode the token and convert from byte to string
        token = base64.urlsafe_b64encode(raw_token).decode('UTF-8')

    except BaseException:
        # @TODO Add more robust exception handling
        flash(strings.ERROR_TOKEN_GENERATION, 'danger')
        return render_template(template)

    # Only send recovery if it is a valid user and token
    if user and token:
        try:
            #print("Sending recovery email to " + user.email_address)

            # Recipients must be an array
            msg = Message(strings.TPL_EMAIL_FORGOT_PASSWORD_SUBJECT, recipients=[user.email_address])

            link = config.WEBSITE_BASE_URL + "/recover-password?token=" + str(token)
            msg.body = strings.TPL_EMAIL_FORGOT_PASSWORD_BODY.replace("{{LINK}}", link)

            mail.send(msg)

            flash(strings.MSG_PASSWORD_RECOVERY_EMAIL_SENT, 'success')
        except BaseException:
            # @TODO Add more robust exception handling
            flash(strings.ERROR_SMTP_FAILURE, 'danger')

    else:
        flash(strings.ERROR_FORGOT_PASSWORD_USER_NOT_FOUND, 'danger')

    return render_template(template)


"""
Special route that takes a magic hash to identify a user and allows
a password change
"""
@anon.route('/recover-password', strict_slashes=False)
def recover_password():
    template = 'newpassword.html'
    raw_token = request.args.get('token')
    token = base64.urlsafe_b64decode(raw_token)

    ## @TODO Refactor to generic token valid func
    s = Serializer(config.IDS_SECRET_KEYS, salt="forgot-password", expires_in=config.IDS_FORGOT_PASSWORD_VALIDITY_TIMER)

    # Try to decode and verify the token timestamp
    try:
        payload = s.loads(token)
        print("Payload: ", payload)
    except SignatureExpired:
        flash(strings.ERROR_TOKEN_EXPIRED, 'danger')
        return redirect(url_for('anon.forgot_password'))
    except BadSignature:
        flash(strings.ERROR_TOKEN_SIGNATURE, 'danger')
        return redirect(url_for('anon.forgot_password'))
    ## end

    #print("Verified Payload: ", payload)

    return render_template(template, token=raw_token)


"""
Reset the password for a user
"""
@anon.route('/recover-password', methods=['POST'])
def recover_password_post():
    raw_token = request.form.get('token')
    token = base64.urlsafe_b64decode(raw_token)
    password1 = request.form.get('password')
    password2 = request.form.get('password2')

    # Verify that the two password strings match
    if password1 != password2:
        flash(strings.ERROR_PASSWORD_MISMATCH, 'danger')
        return redirect(url_for('anon.recover_password', token=raw_token))

    # Check complexity requirements???

    ## @TODO Refactor to generic token valid func
    s = Serializer(config.IDS_SECRET_KEYS, salt="forgot-password", expires_in=config.IDS_FORGOT_PASSWORD_VALIDITY_TIMER)

    # Try to decode and verify the token timestamp
    try:
        payload = s.loads(token)
        print("Payload: ", payload)
    except SignatureExpired:
        flash(strings.ERROR_TOKEN_EXPIRED, 'danger')
        return redirect(url_for('anon.forgot_password'))
    except BadSignature:
        flash(strings.ERROR_TOKEN_SIGNATURE, 'danger')
        return redirect(url_for('anon.forgot_password'))
    ## end

    # Load the user found in the token
    user = User.query.filter_by(user_id=payload['id']).first()

    # If user is found, try to reset password
    if user:
        try:
            user.password = generate_password_hash(password1, method='pbkdf2:sha256:310000', salt_length=128),
            db.session.commit()
            flash(strings.MSG_PASSWORD_RESET, 'success')
        except BaseException:
            # @TODO Add more robust exception handling
            flash(strings.ERROR_PASSWORD_RESET, 'danger')
    else:
        flash(strings.ERROR_PASSWORD_RESET, 'danger')

    return redirect(url_for('anon.login'))























"""
Temporary account creation route to test hash generation

@anon.route('/create-account')
def create_account():
    # code to validate and add user to database goes here
    admin_email_address = 'dinsmorc@oregonstate.edu'
    email_address = 'lunitin@gmail.com'
    first_name = 'Static Test'
    last_name = 'Last'
    password = 'test123'
    security_level = 1


    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email_address=email_address).first()

    # if a user is found, don't create it
    if user:
        flash("Account already exists!")
        return redirect(url_for('anon.login'))

    # create a new user with the form data.
    # Password hash recommendation sizes from:
    # https://en.wikipedia.org/wiki/PBKDF2
    new_user = User(email_address=email_address, first_name=first_name,
            last_name=last_name,
            security_level=0,
            password=generate_password_hash(password, method='pbkdf2:sha256:310000', salt_length=128),
            date_created=datetime.now(),
            date_last_password_change=datetime.now()
            )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Create an admin user
    new_user = User(email_address=admin_email_address, first_name='admin',
            last_name='admin',
            security_level=1,
            password=generate_password_hash(password, method='pbkdf2:sha256:310000', salt_length=128),
            date_created=datetime.now(),
            date_last_password_change=datetime.now()
            )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash("Test accounts " + email_address + " and admin@example.org created")
    return redirect(url_for('anon.login'))

    """
