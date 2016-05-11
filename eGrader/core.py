from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

security = Security()

bootstrap = Bootstrap()

mail = Mail()
