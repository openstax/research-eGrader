import requests

from flask import Blueprint
from flask import abort
from flask import render_template

viewer = Blueprint('viewer',
                   __name__,
                   url_prefix='/viewer',
                   template_folder='../templates/viewer')


EXERCISE_API_URL = 'https://exercises.openstax.org/api/exercises'


def make_exercise_url(exercise_uid):
    return '{0}/{1}.json'.format(EXERCISE_API_URL, exercise_uid)


def get_exercise_json(exercise_uid):
    url = make_exercise_url(exercise_uid)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def get_exercise(exercise_uid):
    data = get_exercise_json(exercise_uid)
    if data:
        exercise_data = data['questions'][0]
        exercise = dict(
            uid=data['uid'],
            exercise_html=exercise_data['stem_html'],
            choices=exercise_data['answers']
        )
        return exercise
    else:
        return None


@viewer.route('/<string:exercise_uid>')
def exercise_viewer(exercise_uid):
    exercise = get_exercise(exercise_uid)
    if exercise:
        return render_template('viewer.html', exercise=exercise)
    else:
        abort(404)
