from app import app
from flask import render_template
import mysql.connector

@app.route('/')
def home():
    # Print a debug to console, requires flush
    print("== Hello from Home", flush=True)
    return "hello world!"


@app.route('/template')
def template():
    return render_template('home.html')

@app.route('/db')
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
