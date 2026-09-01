from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):

    username = StringField(
        "Username",
        render_kw={"placeholder": "Enter username"},
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )

    password = PasswordField(
        "Password",
         render_kw={"placeholder": "Enter password"},
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Login"
    )