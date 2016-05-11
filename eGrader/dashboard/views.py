from flask import Blueprint, render_template
from flask.ext.security import login_required

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard/index.html')
