import numpy as np

from sqlalchemy import and_

from eGrader.algs.active_learning_minvar import train_random_forest, get_min_var_idx
from eGrader.core import db

from sqlalchemy.dialects.postgresql import ARRAY, JSON


def get_next_response(user_id, exercise_id):
    """

    Parameters
    ----------
    user_id
    exercise_id

    Returns
    -------

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
        exercise = Exercise.get_by_id(exercise_id)
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


def get_next_exercise(user_id):
    subquery = db.session.query(ResponseGrade.response_id)\
        .join(Response)\
        .filter(ResponseGrade.user_id == user_id).subquery()
    query = db.session.query(Exercise).join(Response).filter(~Response.id.in_(subquery)).first()

    # Get the JSON exercise data from the exercise.data field
    # This is where the feedback, answers, and other info is located
    e_data = query.data['questions'][0]

    # Create a list for the feedback_choices
    feedback_choices = []

    # Get the correct answer
    for answer in e_data['answers']:
        feedback = (str(answer['id']), answer['feedback_html'])
        feedback_choices.append(feedback)
        if answer['correctness'] == '1.0':
            answer_html = answer['content_html']

    exercise = dict(id=query.id,
                    exercise_html= e_data['stem_html'],
                    answer_html=answer_html,
                    feedback_choices=feedback_choices
                    )
    return exercise


class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer(), primary_key=True)
    external_id = db.Column(db.Integer())           # X.1
    deidentifier = db.Column(db.String())           # Deidentifier
    free_response = db.Column(db.Text())            # Free.Response
    correct = db.Column(db.Boolean())               # Correct.
    correct_answer_id = db.Column(db.Integer())     # Correct.Answer.Id
    exercise_type = db.Column(db.String())          # Exercise.type
    exercise_id = db.Column(db.Integer(), db.ForeignKey('exercises.id'))

    @classmethod
    def get_by_id(cls, id):
        return db.session.query(cls).filter(cls.id == id).first()

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
    def get_by_id(cls, id):
        return db.session.query(cls).filter(cls.id == id).first()


class ResponseGrade(db.Model):
    ___tablename__= 'response_grades'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    response_id = db.Column(db.Integer(), db.ForeignKey('responses.id'))
    score = db.Column(db.Float())
    misconception = db.Column(db.Boolean())
    junk = db.Column(db.Boolean())
    feedback_id = db.Column(db.Integer())

    @classmethod
    def get_grades(cls, user_id, exercise_id):
        query = db.session.query(Response.id, cls.junk)\
            .outerjoin(cls, and_(cls.response_id == Response.id, cls.user_id == user_id))\
            .filter(Response.exercise_id == exercise_id)
        return query.all()
