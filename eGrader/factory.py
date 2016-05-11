from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .accounts.models import User, Role
from .core import bootstrap, db, security, mail
from .dashboard.views import dashboard
from .grader.views import grader
from .redis_session import RedisSessionInterface


def create_app(package_name, package_path, settings=None):
    app = Flask(package_name,
                instance_relative_config=True,
                template_folder='templates')
    app.config.from_pyfile('conf.py', silent=True)
    app.config.from_object('eGrader.security_config')

    if settings is not None:
        app.config.from_object(settings)

    # init extensions
    db.init_app(app)
    security.init_app(app,
                      SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=True)
    bootstrap.init_app(app)
    mail.init_app(app)

    # attach redis sessions
    app.session_interface = RedisSessionInterface()

    # register main blueprints
    app.register_blueprint(dashboard)
    app.register_blueprint(grader)

    return app
