from flask import abort, Blueprint, jsonify, request

from eGrader.core import db
from eGrader.grader.models import get_next_exercise_id, get_parsed_exercise, Response, ResponseGrade

api = Blueprint('api',
                __name__,
                url_prefix='/api/v1')


@api.route('/ping')
def pong():
    return jsonify(dict(message='pong'))


@api.route('/exercises/<int:exercise_id>')
def get_exercise(exercise_id):
    exercise = get_parsed_exercise(exercise_id)
    if not exercise:
        abort(404)
    else:
        return jsonify(**exercise)


@api.route('/exercise/next', methods=['GET'])
def get_next_exercise():
    user_id = request.args.get('user_id', None)
    exercise_id = get_next_exercise_id(user_id)
    if not exercise_id:
        return jsonify(dict(success=False, message='There are no more exercises for that user'))
    else:
        return jsonify(dict(success=True, exercise_id=exercise_id))


@api.route('/response/next', methods=['GET'])
def next_response():
    from eGrader.grader.models import get_next_response

    user_id = request.args.get('user_id', None)
    exercise_id = request.args.get('exercise_id', None)
    try:
        response = get_next_response(user_id, exercise_id)
    except Exception:
        return jsonify(dict(
            message='There are no more responses available for that exercise',
            success=False))
    return jsonify(dict(success=True, response=response.to_json()))


@api.route('/response/submit', methods=['POST'])
def submit_grader_response():
    posted = request.get_json()
    print(posted)
    grade = ResponseGrade(
        user_id = posted['user_id'] if posted['user_id'] else None,
        response_id=posted['responseId'] if posted['responseId'] else None,
        score=posted['score'] if 'score' in posted else None,
        misconception = posted['misconception'] if 'misconception' in posted else None,
        junk = posted['quality'],
        feedback_id = posted['feedback_id'] if posted['quality'] else None
    )
    db.session.add(grade)
    db.session.commit()

    return jsonify(dict(success=True, message='Response submitted'))