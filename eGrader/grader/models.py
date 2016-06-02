import numpy as np

from sqlalchemy import and_, func
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.sql.expression import extract, label

from eGrader.algs.active_learning_minvar import train_random_forest, get_min_var_idx
from eGrader.core import db



from eGrader.utils import JsonSerializer


def get_next_response(user_id, exercise_id):
    """

    Parameters
    ----------
    user_id
    exercise_id

    Returns
    -------
    response
        The response object from a list of responses

    """
    # TODO: Finish docstring of get_next_response function

    grades = ResponseGrade.get_grades(user_id, exercise_id)
    print('Printing Grades: ',grades)

    labels = [grade[1] for grade in grades]
    labels_array = np.array(labels, dtype=float)

    if all(v is None for v in labels):
        response = Response.get_first_ungraded_response(user_id, exercise_id)

        return response
    else:
        exercise = Exercise.get(exercise_id)
        responses = Response.all_by_exercise_id(exercise_id)
        forest_name = exercise.forest_name
        if forest_name:
            # Load forest and get next best response
            print('load forest')
        else:
            # Create random forest, predict best response, and save to disk.
            # TODO: save forest to disk
            features = np.array(exercise.features)
            obs_idx = np.where(~np.isnan(labels_array))[0]
            print obs_idx
            forest = train_random_forest(features[obs_idx], labels_array[obs_idx])
            print forest
            prediction_idx = get_min_var_idx(features, labels_array, forest)

        return responses[prediction_idx]


def get_next_exercise_id(user_id):
    """
    Get the next exercise with responses that the grader is able to grade.
    Parameters
    ----------
    user_id:int
        the id of the user

    Returns
    -------
    exercise_id: int
        the exercise id of the next exercise that has responses to grade
    """
    # Create a subquery of all responses graded by the user
    subquery = db.session.query(ResponseGrade.response_id)\
        .join(Response)\
        .filter(ResponseGrade.user_id == user_id).subquery()
    # Return the first exercise that has responses not in the the subquery
    ex_r = db.session.query(Exercise).join(Response).filter(~Response.id.in_(subquery)).first()

    return ex_r.id


def get_parsed_exercise(exercise_id):
    # Get the JSON exercise data from the exercise.data field
    # This is where the feedback, answers, and other info is located

    exercise = Exercise.get(exercise_id)

    e_data = exercise.data['questions'][0]

    # Create a list for the feedback_choices
    feedback_choices = []

    # Get the correct answer
    for answer in e_data['answers']:
        feedback = (str(answer['id']), answer['feedback_html'])
        feedback_choices.append(feedback)
        if answer['correctness'] == '1.0':
            answer_html = answer['content_html']

    return dict(id=exercise.id,
                exercise_html=e_data['stem_html'],
                answer_html=answer_html,
                feedback_choices=feedback_choices
                )


def get_grading_session_metrics(user_id):
    subq = db.session.query(ResponseGrade.session_id.label('session_id'),
                            func.count(ResponseGrade.id).label('responses_graded'),
                            label('time_grading', UserGradingSession.ended_on - UserGradingSession.started_on)) \
        .join(UserGradingSession) \
        .filter(UserGradingSession.user_id == user_id) \
        .group_by(ResponseGrade.session_id,
                  UserGradingSession.started_on,
                  UserGradingSession.ended_on).subquery()

    query = db.session.query(func.count(subq.c.session_id),
                             func.sum(subq.c.responses_graded),
                             extract('EPOCH', func.sum(subq.c.time_grading)))

    return query.all()[0]


class Response(db.Model, JsonSerializer):
    __tablename__ = 'responses'
    id = db.Column(db.Integer(), primary_key=True)  # The corresponding columns in the spreadsheet
    external_id = db.Column(db.Integer())           # X.1
    deidentifier = db.Column(db.String())           # Deidentifier
    free_response = db.Column(db.Text())            # Free.Response
    correct = db.Column(db.Boolean())               # Correct.
    correct_answer_id = db.Column(db.Integer())     # Correct.Answer.Id
    exercise_type = db.Column(db.String())          # Exercise.type
    exercise_id = db.Column(db.Integer(), db.ForeignKey('exercises.id'))

    @classmethod
    def get(cls, response_id):
        return db.session.query(cls).get(response_id)

    @classmethod
    def all_by_exercise_id(cls, exercise_id):
        return db.session.query(cls)\
            .filter(cls.exercise_id == exercise_id)\
            .order_by(cls.id)\
            .all()

    @classmethod
    def get_first_ungraded_response(cls, user_id, exercise_id):
        subquery = db.session.query(ResponseGrade.response_id) \
            .join(Response).filter(ResponseGrade.user_id == user_id).subquery()
        query = db.session.query(Response).filter(Response.exercise_id == exercise_id) \
            .filter(~Response.id.in_(subquery))
        return query.first()


class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer(), primary_key=True)
    uid = db.Column(db.String(), unique=True)
    url = db.Column(db.String())
    api_url = db.Column(db.String())  # API.URL
    data = db.Column(JSON())
    version = db.Column(db.Integer())
    features = db.Column(ARRAY(db.Integer()))
    forest_name = db.Column(db.String())

    @classmethod
    def get(cls, exercise_id):
        return db.session.query(cls).get(exercise_id)


class ResponseGrade(db.Model):
    ___tablename__= 'response_grades'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    response_id = db.Column(db.Integer(), db.ForeignKey('responses.id'))
    score = db.Column(db.Float())
    misconception = db.Column(db.Boolean())
    junk = db.Column(db.Boolean())
    feedback_id = db.Column(db.Integer())
    submitted_on = db.Column(db.DateTime())
    session_id = db.Column(db.Integer(), db.ForeignKey('user_grading_sessions.id'))

    @classmethod
    def get_grades(cls, user_id, exercise_id):
        query = db.session.query(Response.id, cls.junk)\
            .outerjoin(cls, and_(cls.response_id == Response.id, cls.user_id == user_id))\
            .filter(Response.exercise_id == exercise_id)
        return query.all()

    @classmethod
    def by_user_id(cls, user_id):
        return db.session.query(cls).filter(cls.user_id == user_id).all()


class ExerciseNotes(db.Model, JsonSerializer):
    __tablename__ = 'user_exercise_notes'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    exercise_id = db.Column(db.Integer(), db.ForeignKey('exercises.id'))
    text = db.Column(db.Text())


class UserGradingSession(db.Model, JsonSerializer):
    __tablename__ = 'user_grading_sessions'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    started_on = db.Column(db.DateTime())
    ended_on = db.Column(db.DateTime())

    @classmethod
    def by_user_id(cls, user_id):
        return db.session.query(cls).filter(cls.user_id == user_id).all()


    @classmethod
    def latest(cls, user_id):
        return db.session.query(cls)\
            .filter(cls.user_id == user_id)\
            .filter(cls.ended_on != None)\
            .order_by(cls.ended_on.desc())\
            .first()
