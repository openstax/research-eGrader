from flask.ext.socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack

db = SQLAlchemy()

security = Security()

bootstrap = Bootstrap()

mail = Mail()

webpack = Webpack()

socketio = SocketIO()
