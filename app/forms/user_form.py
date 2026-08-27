from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,SelectField
from wtforms.validators import DataRequired, Length, EqualTo


class UserForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(max=50)           
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=200)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("Admin", "Admin"),
            ("Librarian", "Librarian")
        ],
        default="Librarian",
        validators=[
            DataRequired()
        ]
    )

    status = SelectField(
        "Status",
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        validators=[DataRequired()]
    )

    submit = SubmitField(
            "Save"
        )