from instance import secret_settings

# Secrets are kept in a secret_settings.py file for development purposes
# When this application is deployed by ansible the proper values are written in via template.
SQLALCHEMY_DATABASE_URI = secret_settings.SQL_ALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO=False
LOG_PATH = '/var/www/log/labs-flask.log'
SECRET_KEY = secret_settings.SECRET_KEY
DEBUG = True
MAIL_PASSWORD = secret_settings.MAIL_PASSWORD
MAIL_SERVER = secret_settings.MAIL_SERVER
MAIL_USERNAME = secret_settings.MAIL_USERNAME
WEBPACK_MANIFEST_PATH = '../eGrader/static/manifest.json'
SECURITY_PASSWORD_SALT = secret_settings.SECURITY_PASSWORD_SALT
# WEBPACK_ASSETS_URL = 'http://127.0.0.1:5011/static/build/'
