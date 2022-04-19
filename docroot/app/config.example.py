""" config.example.py

Environmental configuration parameters

These values may vary based upon installation environment.

This file should have all of the same parameters as in config.py but sanitized.

"""

# Web Application URL - no trailing slash
WEBSITE_BASE_URL = "http://localhost:8080"

# Flask-Session Configuration
SESSION_KEY = "secure.session.key"

# SQLAlchemy Configuration
MYSQL_URI = 'mysql://username:password@host/database'

# Flask-Mail Configuration
MAIL_SERVER = "localhost"
MAIL_PORT = "25"
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = "sender@example.org"
MAIL_DEBUG = False

# itsdangerous Configuration
# Multiple keys will be used in order and can be rotated out over time
# See https://itsdangerous.palletsprojects.com/en/2.1.x/concepts/#key-rotation
IDS_SECRET_KEYS = ["secret.code.here"]

IDS_FORGOT_PASSWORD_VALIDITY_TIMER = 1800 # seconds
