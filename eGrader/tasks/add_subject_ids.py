from eGrader import create_app

from eGrader.core import db

from eGrader.models import Exercise, Response



def update_exercises_with_subject():

    subjects = dict(
        apbio=1,
        k12phys=2
    )

    exercises = db.session.query(Exercise).all()

    for exercise in exercises:
        tags = exercise.data['tags']
        if 'apbio' in tags:
            exercise.subject_id = subjects['apbio']
        elif 'k12phys' in tags:
            exercise.subject_id = subjects['k12phys']
        db.session.add(exercise)
    db.session.commit()


def update_responses_with_subject():
    subjects = dict(
        apbio=1,
        k12phys=2
    )

    responses = db.session.query(Response).all()

    for response in responses:
        print(response.id)
        exercise = db.session.query(Exercise).filter(Exercise.id == response.exercise_id).first()
        tags = exercise.data['tags']

        if 'apbio' in tags:
            response.subject_id = subjects['apbio']
        elif 'k12phys' in tags:
            response.subject_id = subjects['k12phys']

        db.session.add(response)
    db.session.commit()
