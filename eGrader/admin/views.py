from flask import Blueprint, render_template
from flask.ext.principal import Permission, RoleNeed

from eGrader.admin.exports import (list_graded_responses,
                                   list_exercises,
                                   list_sessions,
                                   list_users,
                                   list_responses)
from eGrader.utils import render_csv

admin_permission = Permission(RoleNeed('admin'))

admin = Blueprint('admin',
                  __name__,
                  template_folder='../templates/admin'
                  )


@admin.route('/admin', methods=['GET'])
@admin_permission.require()
def index():
    return render_template('admin_index.html', active_page='index')


@admin.route('/admin/export', methods=['GET'])
def export():
    return render_template('admin_exports.html', active_page='export')


@admin.route('/admin/export/grades')
@admin_permission.require()
def export_graded_responses():
    grades = list_graded_responses()
    atts = ['id',
            'step_id',
            'user_id',
            'email',
            'response_id',
            'score',
            'misconception',
            'junk',
            'feedback_id',
            'session_id',
            'submitted_on']
    return render_csv(atts, grades, 'graded-responses')


@admin.route('/admin/export/exercises')
@admin_permission.require()
def export_exercises():
    exercises = list_exercises()
    atts = ['id',
            'uid',
            'url',
            'subject',
            'chapter_id',
            'section_id']
    return render_csv(atts, exercises, 'exercises')


@admin.route('/admin/export/sessions')
@admin_permission.require()
def export_sessions():
    sessions = list_sessions()
    atts = ['session_id',
            'user_id',
            'email',
            'started_on',
            'ended_on']

    return render_csv(atts, sessions, 'grading-sessions')


@admin.route('/admin/export/users')
@admin_permission.require()
def export_users():
    users = list_users()
    atts = ['id',
            'email',
            'last_login_at',
            'login_count',
            'subject',
            'active']

    return render_csv(atts, users, 'users')


@admin.route('/admin/export/responses')
@admin_permission.require()
def export_responses():
    responses = list_responses()
    atts = ['id',
            'exercise_id',
            'step_id',
            'subject',
            'free_response',
            'correct',
            'correct_answer_id',
            'deidentifier']

    return render_csv(atts, responses, 'responses')
