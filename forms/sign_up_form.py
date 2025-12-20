from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

from wtforms.validators import EqualTo

class Signup(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[DataRequired(), Length(min=2, max=30)]
    )

    last_name = StringField(
        'Last Name',
        validators=[DataRequired(), Length(min=2, max=30)]
    )

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Sign Up')
