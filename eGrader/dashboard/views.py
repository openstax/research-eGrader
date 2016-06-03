from flask import Blueprint, render_template
from flask.ext.login import current_user
from flask.ext.security import login_required

from eGrader.grader.models import ResponseGrade, UserGradingSession, get_grading_session_metrics

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
@login_required
def index():
    # Number of Sessions, Number of Responses, Total time
    # [(3L, Decimal('13'), 5314.563611)]
    grading_session_metrics = get_grading_session_metrics(current_user.id)
    print(grading_session_metrics)
    if grading_session_metrics[0]:
        total_responses = grading_session_metrics[1]
        total_sessions = grading_session_metrics[0]

        data = dict(
            total_responses=total_responses,
            avg_graded_per_session=total_responses / total_sessions,
            total_time_grading=grading_session_metrics[2] / 60,
            response_grading_rate=(int(grading_session_metrics[2] / 60) / total_responses)
        )
    else:
        data = dict(
            total_responses=0,
            avg_graded_per_session=0,
            total_time_grading=0,
            response_grading_rate=0
        )

    return render_template('dashboard/index.html', data=data)
