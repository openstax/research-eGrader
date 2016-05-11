import flask_wtf as WTF
from wtforms import SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired

quality_choices = [('t', 'Junk'), ('f', 'Not Junk')]
scores = [('0', 'No Credit'), ('1', 'Full Credit'), ('.5', 'Partial Credit')]
misconception = [('t', 'Yes'), ('f', 'No')]


class RequiredIf(DataRequired):
    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if not bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class GraderForm(WTF.Form):
    response_id = HiddenField('Response ID')
    quality = SelectField(u'Quality',
                          validators=[DataRequired()],
                          choices=quality_choices)
    score = SelectField(u'Score',
                        validators=[RequiredIf('quality')],
                        choices=scores)
    misconception = SelectField(u'Misconception',
                                validators=[RequiredIf('quality')], choices=misconception)
    feedback = SelectField(u'Feedback',
                           validators=[RequiredIf('quality')])
    submit = SubmitField()
