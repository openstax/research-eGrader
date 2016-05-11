import json

from flask import Blueprint, render_template, request, redirect, session, url_for
from flask.ext.login import login_required
from flask.ext.security import current_user

from eGrader.grader.forms import GraderForm
from ..core import db

from .models import Exercise, Response, ResponseGrade, get_next_response, get_next_exercise

grader = Blueprint('grader',
                   __name__,
                   url_prefix='/grader',
                   template_folder='../templates/grader')


def _get_exercise_response():
    user_id = current_user.id
    if 'exercise' in session and session['exercise']:
        exercise = session['exercise']
    else:
        exercise = get_next_exercise(user_id)
        print ('Printing exercise_id!', exercise['id'])

    if 'response' in session and session['response']:
        response = session['response']
    else:
        response = get_next_response(user_id, exercise['id'])
        print ('Printing exercise_id!', exercise['id'])

    if not response:
        _get_exercise_response()

    return exercise, response


@grader.route('/', methods=['GET', 'POST'])
@login_required
def grade_next_response():
    # In this case, `exercise` is a dictionary and response is a Model Class. Some extra work was done on
    # exercise to make it easier to work with.
    exercise, response = _get_exercise_response()

    form = GraderForm(request.form)

    if request.method == 'POST':
        form.feedback.choices = [(choice[0], choice[0]) for choice in exercise['feedback_choices']]
        if form.validate():
            grade = ResponseGrade(
                response_id = form.response_id.data,
                user_id = current_user.id,
                score = form.score.data,
                misconception = form.misconception.data,
                junk = form.quality.data,
                feedback_id = form.feedback.data
            )
            db.session.add(grade)
            db.session.commit()
            # Clear the session of the response
            session['response'] = None
            return redirect(url_for('grader.grade_next_response'))

    free_response = response.free_response
    form.feedback.choices = exercise['feedback_choices']
    form.response_id.data = response.id

    return render_template('grader_index.html', form=form,
                           exercise=exercise,
                           free_response = free_response)

