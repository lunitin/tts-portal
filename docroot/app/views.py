""" views.py

LEGACY CODE FOR REFERENCE - NOT USED

"""

from app import app
from flask import request, jsonify, make_response, render_template
from functools import wraps
import mysql.connector
import jwt


"""
::: AUTHENTICATION ROUTES & PROCEDURES :::
"""


"""
Decorator route to apply auth required
"""
def auth_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']

       if not token:
           print("== no token present", flush=True)
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

           print("== JWT data", data)
           return jsonify(data)
       # if failed to decode there is an error
       except:
           print("== Failed to decode token", flush=True)
           return redirect("/login", code=302)
           #return jsonify({'message': 'token is invalid'})

       return f(current_user, *args, **kwargs)
   return decorator



@app.route('/login', methods=['GET'])
def login_form():
    # Print a debug to console, requires flush
    print("== Hello from Login", flush=True)
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
   # Print a debug to console, requires flush
   print("== Hello from Do Login", flush=True)
   print(request)
   # If we have a token why login?
   #auth = request.authorization
   #if not auth or not auth.username or not auth.password:
   #   return make_response('could not verify', 401, {'Authentication': 'login required"'})

   token = jwt.encode({'username' : "test1", 'group' : "users"}, app.config['SECRET_KEY'], "HS256")

   #return jsonify({'token' : token })
   return make_response(jsonify({'token' : token}), 201)


"""
::: END AUTHENTICATION ROUTES & PROCEDURES :::
"""

"""
::: EXAMPLE ROUTES :::
"""

@app.route('/')
def home():
    # Print a debug to console, requires flush
    print("== Hello from Home", flush=True)
    return "hello world!"


@app.route('/template')
def template():
    return render_template('home.html')

@app.route('/db')
@auth_required
def db():
    # Connect to the database and perform a query
    cnx = mysql.connector.connect(user='root', password='beastm0de',
                                  host='db')
    cursor = cnx.cursor()

    query = ("SELECT first_name FROM tts_portal.users")
    cursor.execute(query)

    text = "User Accounts<br>"

    if not cursor.rowcount:
        print("No results found")
    else:
        for row in cursor:
            print(row)
            text += ', '.join(row)
            text += "<br>"

    cursor.close()

    cnx.close()
    return text