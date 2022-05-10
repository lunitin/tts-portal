""" strings.py

Error and message strings and templates

"""

WEBSITE_HTML_TITLE_TRAILER = ": Traffic Technology Services"

# Errors
ERROR_USER_NOT_FOUND_INVALID_PASS = "Please check your login details and try again."
ERROR_TOKEN_GENERATION = "Error generating token, contact your administrator."
ERROR_TOKEN_SIGNATURE = "Token signature is invalid, please try again."
ERROR_TOKEN_EXPIRED = "Token expired, please try again."
ERROR_SMTP_FAILURE = "Could not send email message, contact your administrator."
ERROR_PASSWORD_MISMATCH = "Passwords do not match."
ERROR_PASSWORD_RESET = "Your password could not be reset, contact your administrator."
ERROR_PAGE_PERMISSION_DENIED = "You do not have permission to view that page"

ERROR_USER_DNE = "User does not exist!"
ERROR_COVERAGE_DNE = "Coverage does not exist!"
# @TODO Ideally this should match MSG_PASSWORD_RECOVERY_EMAIL_SENT to prevent username disclosure
#ERROR_FORGOT_PASSWORD_USER_NOT_FOUND = 'A recovery message has been sent to your email address'
ERROR_FORGOT_PASSWORD_USER_NOT_FOUND = 'E-mail address not found'

# Status Messages
MSG_LOGIN_WELCOME_BACK = "You are logged in, welcome back!"
MSG_PASSWORD_RECOVERY_EMAIL_SENT = 'A recovery message has been sent to your email address'
MSG_PASSWORD_RESET = "Your password has been reset, please log in using your new credentials."

MSG_USER_DELETED = "User deleted Successfully"
MSG_COVERAGE_DELETED = "Coverage deleted Successfully"
MSG_REGION_DELETED = "Region deleted Successfully"

MSG_USER_CREATED = "User created Successfully"
MSG_COVERAGE_CREATED = "Coverage created Successfully"
MSG_REGION_CREATED = "Region created Successfully"

MSG_REGION_REMOVED = "Region removed"
# Templates may/may not contain placeholders
TPL_EMAIL_FORGOT_PASSWORD_SUBJECT = "TTS Portal Password Recovery"
TPL_EMAIL_FORGOT_PASSWORD_BODY = """
There has been a request to reset the password to your TTS Portal account.

Click the link below or paste it into a browser to reset your password.

{{LINK}}

This link will expire in 30 minutes.

If you did not request this password change contact the TTS Administrator

"""
TPL_USER_UPDATED = "User {name}, was updated."
TPL_USER_CREATED = "Account {email} was created!"
TPL_EXISTING_EMAIL = "{email} already in use."

TPL_ADD_USERS_TO_COVERAGE = "User(s) were successfully added to {coverage}."
TPL_ERROR_USER_TO_COVERAGE = "{user} was not added to {coverage}"

TPL_DEL_USER_ACCESS= "{user}'s access to {coverage} has been removed."
TPL_ERR_DEL_USER_ACCESS= "Unable to remove {user}'s access to {coverage}."

TPL_REGION_TO_COVERAGE = "Region Added to {coverage} Successfully."
TPL_ERR_REGION_TO_COVERAGE = "Unable to add {region} to {coverage}."