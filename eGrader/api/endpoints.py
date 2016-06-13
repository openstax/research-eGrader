from datetime import datetime
from flask import abort, Blueprint, jsonify, request

from eGrader.core import db

from eGrader.accounts.models import User

from eGrader.grader.models import (ExerciseNote,
                                   get_next_exercise_id,
                                   get_parsed_exercise,
                                   Response,
                                   ResponseGrade,
                                   UserGradingSession,
                                   UserUnqualifiedExercise)


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
    chapter_id = request.args.get('chapter_id', None)
    user = User.get(user_id)

    exercise_id = get_next_exercise_id(user_id, user.subject_id, chapter_id=chapter_id, random=True)

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
    except ValueError:
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
        feedback_id = posted['feedback_id'] if posted['quality'] else None,
        submitted_on = datetime.utcnow(),
        session_id = posted['session_id']
    )
    db.session.add(grade)
    db.session.commit()

    return jsonify(dict(success=True, message='Response submitted'))


@api.route('/exercise/unqualified', methods=['POST'])
def not_qualified():
    posted = request.get_json()
    unqual = UserUnqualifiedExercise(
        user_id = posted['user_id'],
        exercise_id = posted['exercise_id']
    )
    db.session.add(unqual)
    db.session.commit()

    return jsonify(dict(success=True, message='Qualification submitted'))


@api.route('/exercise/notes', methods=['GET'])
def get_user_exercise_notes():
    user_id = request.args.get('user_id', None)
    exercise_id = request.args.get('exercise_id', None)
    notes = ExerciseNote.get_by_user_id(user_id, exercise_id)
    data = [{"id": note.id,
             "text": note.text} for note in notes]

    if not notes:
        return jsonify(dict(success=False, notes=[]))
    else:
        return jsonify(dict(success=True, notes=data))


@api.route('/exercise/notes', methods=['POST'])
def submit_note():
    posted = request.get_json()
    note = ExerciseNote(
        user_id = posted['user_id'],
        exercise_id = posted['exercise_id'],
        text = posted['text'],
        created_on = datetime.utcnow()
    )

    db.session.add(note)
    db.session.commit()

    return jsonify(dict(success=True, message='Note submitted', note=note.to_json()))
