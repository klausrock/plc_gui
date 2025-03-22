from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    license_number = PasswordField(
        'License Number',
        validators=[
            DataRequired(),
            Length(min=1, max=64, message="License number must be between 1 and 64 characters.")
        ]
    )
    log_in = SubmitField('Log In')