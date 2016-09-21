from datetime import datetime
from flask import Blueprint, render_template
from flask_login import current_user
from flask_security import login_required

from eGrader.core import db
from eGrader.grader.models import (get_grading_session_details,
                                   get_grading_session_metrics,
                                   ResponseGrade,
                                   UserGradingSession
                                   )

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
@login_required
def index():
    # Number of Sessions, Number of Responses, Total time
    # [(3L, Decimal('13'), 5314.563611)]

    last_session = UserGradingSession.latest_by_start(current_user.id)

    if last_session and not last_session.ended_on:
        latest_response = ResponseGrade.latest_by_session_id(last_session.id)
        if latest_response:
            last_session.ended_on = latest_response.submitted_on
            db.session.add(last_session)
            db.session.commit()

    grading_session_metrics = get_grading_session_metrics(current_user.id)
    grading_session_details = get_grading_session_details(current_user.id)

    if grading_session_metrics[0]:
        total_responses = grading_session_metrics[1]
        total_sessions = grading_session_metrics[0]
        try:
            data = dict(
                total_responses=total_responses,
                avg_graded_per_session=total_responses / total_sessions,
                total_time_grading=grading_session_metrics[2] / 60,
                response_grading_rate=(total_responses / int(grading_session_metrics[2] / 60))
            )
        except Exception:
            data = dict(
                total_responses=0,
                avg_graded_per_session=0,
                total_time_grading=0,
                response_grading_rate=0
            )
    else:
        data = dict(
            total_responses=0,
            avg_graded_per_session=0,
            total_time_grading=0,
            response_grading_rate=0
        )

    if grading_session_details:
        sessions = []
        for item in grading_session_details:
            session = dict(response_count=item[1],
                           started_on=item[2],
                           ended_on=item[3],
                           time_grading=item[4])
            sessions.append(session)
    else:
        sessions = []

    return render_template('dashboard/index.html', data=data, sessions=sessions)
