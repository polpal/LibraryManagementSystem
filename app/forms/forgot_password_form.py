from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField,StringField
from wtforms.validators import DataRequired, Email

class ForgotPasswordForm(FlaskForm):


    username = StringField(
    "Username",
    validators=[
        DataRequired()
    ]
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    submit = SubmitField(
        "Send Reset Link"
    )