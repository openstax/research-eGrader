from datetime import datetime
from flask import url_for
from flask.ext.script import Manager
from flask.ext.security import utils

from eGrader import create_app
from eGrader.models import *
from eGrader.core import db

app = create_app()
manager = Manager(app)


@manager.command
def create_db():
    db.create_all()
    db.session.commit()
    print ('Database has been created')


@manager.command
def drop_db():
    db.drop_all()
    db.session.commit()
    print ('Database has been dropped')


@manager.command
def reset_db():
    drop_db()
    create_db()
    print ('Database has been reset')


@manager.command
def load_exercise_features():
    from eGrader.tasks.prepare_response_matrix import load_exercise_features
    load_exercise_features()
    return

@manager.command
def load_subject_ids():
    from eGrader.tasks.add_subject_ids import update_responses_with_subject, update_exercises_with_subject
    update_exercises_with_subject()
    update_responses_with_subject()
    return

@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
def create_admin_user(email, password):
    user_datastore = app.extensions['security'].datastore
    user_datastore.find_or_create_role(name='admin',
                                       description='Administrator')
    encrypted_password = utils.encrypt_password(password)

    if not user_datastore.get_user(email):
        user_datastore.create_user(email=email,
                                   active=True,
                                   registered_at=datetime.now(),
                                   confirmed_at=datetime.now(),
                                   password=encrypted_password)
    db.session.commit()
    user_datastore.add_role_to_user(email, 'admin')
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
@manager.option('-s', '--subject_id', dest='subject_id')
def create_user(email, password, subject_id):

    user_datastore = app.extensions['security'].datastore

    encrypted_password = utils.encrypt_password(password)

    if not user_datastore.get_user(email):
        user_datastore.create_user(email=email,
                                   active=True,
                                   registered_at=datetime.now(),
                                   confirmed_at=datetime.now(),
                                   password=encrypted_password,
                                   subject_id=subject_id)
    db.session.commit()


@manager.command
def send_test_email():
    from flask.ext.mail import Message
    from eGrader.core import mail

    to = ['labs@openstax.org']
    subject = 'Test Email'
    template = '<h1>This is a test of Openstax eGrader email messaging system</h1>'

    msg = Message(
        subject,
        recipients=to,
        html=template,
        sender=app.config['SECURITY_EMAIL_SENDER']
    )
    mail.send(msg)


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:30s} {}".format(
            rule.endpoint,
            methods,
            url))
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()
