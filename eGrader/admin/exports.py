from eGrader.core import db
from eGrader.models import ResponseGrade, Response, Exercise, Subject, UserGradingSession, User

admin_users = [3, 9, 10, 11, 12, 20, 24, 25, 26]


def list_graded_responses():
    grades = db.session.query(ResponseGrade.id,
                              Response.step_id,
                              ResponseGrade.user_id,
                              User.email,
                              ResponseGrade.response_id,
                              ResponseGrade.score,
                              ResponseGrade.misconception,
                              ResponseGrade.junk,
                              ResponseGrade.feedback_id,
                              ResponseGrade.session_id,
                              ResponseGrade.submitted_on)

    grades = grades\
        .join(Response)\
        .join(User)

    grades = grades.filter(~ResponseGrade.user_id.in_(admin_users))

    return grades.all()


def list_exercises():
    exercises = db.session.query(Exercise.id,
                                 Exercise.uid,
                                 Exercise.url,
                                 Subject.name.label('subject'),
                                 Exercise.chapter_id,
                                 Exercise.section_id).join(Subject)
    return exercises.all()


def list_sessions():
    sessions = db.session.query(UserGradingSession.id.label('session_id'),
                                UserGradingSession.user_id,
                                User.email,
                                UserGradingSession.started_on,
                                UserGradingSession.ended_on).join(User)
    sessions = sessions.filter(~User.id.in_(admin_users))

    return sessions.all()


def list_users():
    users = db.session.query(User.id,
                             User.email,
                             User.last_login_at,
                             User.login_count,
                             Subject.name.label('subject'),
                             User.active
                             ).join(Subject)
    return users.all()


def list_responses():
    responses = db.session.query(Response.id,
                                 Response.exercise_id,
                                 Response.step_id,
                                 Subject.name.label('subject'),
                                 Response.free_response,
                                 Response.correct,
                                 Response.correct_answer_id,
                                 Response.deidentifier
                                 ).join(Subject)

    return responses.all()


def list_all_results():
    results = db.session.query(Response.id.label('response_id'),
                           Response.step_id,
                           Response.deidentifier,
                           User.id.label('user_id'),
                           ResponseGrade.score,
                           ResponseGrade.junk,
                           ResponseGrade.misconception,
                           Response.free_response,
                           Response.subject_id,
                           Subject.name.label('subject_name'),
                           Response.exercise_id,
                           Exercise.uid,
                           Exercise.api_url,
                           Exercise.chapter_id,
                           Exercise.section_id,
                           Response.correct,
                           ResponseGrade.submitted_on
    ).join(ResponseGrade).join(User).join(Exercise).join(Subject)

    results = results.filter(~User.id.in_(admin_users))

    return results.all()
