from eGrader.core import db
from eGrader.models import Role, Subject

def get_subject_choices():
    subjects = db.session.query(Subject).all()
    subject_choices = [(str(sub.id), sub.name) for sub in subjects]
    subject_choices.insert(0, ('', 'None'))

    return subject_choices


def get_role_choices():
    roles = db.session.query(Role).all()
    role_choices = [(str(role.id), role.name) for role in roles]
    role_choices.insert(0, ('', 'None'))

    return role_choices
