from flask_security.forms import ConfirmRegisterForm

import flask_wtf as WTF
from wtforms import SelectField, SubmitField, HiddenField, StringField
from wtforms.validators import DataRequired

subject_choices = [('1', 'Biology'), ('2', 'Physics')]

class ExtendedRegisterForm(ConfirmRegisterForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    subject_id = SelectField('Subject', choices=subject_choices)
