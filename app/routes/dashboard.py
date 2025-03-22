from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('dashboard', __name__, url_prefix='')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('views/dashboard/index.html')

@bp.route('system-settings')
@login_required
def system_settings():
    return render_template('views/dashboard/system_settings.html')