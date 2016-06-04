from instance.conf import (MAIL_PASSWORD,
                           MAIL_SERVER,
                           MAIL_USERNAME,
                           SECURITY_PASSWORD_SALT)

SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = SECURITY_PASSWORD_SALT
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_EMAIL_SENDER = 'Openstax eGrader <noreply@openstax.org>'
MAIL_SERVER = MAIL_SERVER
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = MAIL_USERNAME
MAIL_PASSWORD = MAIL_PASSWORD
