from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth import LoginForm
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='')

@bp.route('/', methods=['GET', 'POST'])
def login():
    # Redirect logged-in users to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        license_number = form.license_number.data

        # Check if the license_number exists in the database
        user = User.query.filter_by(license_number=license_number).first()

        if user:
            login_user(user)
            flash("Successfully logged in!", "success")
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Invalid license number. Please try again.", "danger")

    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))