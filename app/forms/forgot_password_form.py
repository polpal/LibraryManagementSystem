from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired, Email

class ForgotPasswordForm(FlaskForm):

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