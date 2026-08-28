from dataclasses import field
from app.models import User, user
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,SelectField
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    Email,
    ValidationError
)


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

    email = StringField(
    "Email",
    validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ]
)

    phone = StringField(
    "Phone",
    validators=[
        DataRequired(),
        Length(min=10, max=20)
    ]
)

    submit = SubmitField(
            "Save"
        )
    def validate_username(self, field):

        user = User.query.filter_by(
        username=field.data
    ).first()

        if user:

            raise ValidationError(
            "Username already exists."
        )
    
    def validate_email(self, field):

        user = User.query.filter_by(
        email=field.data
    ).first()

        if user:

            raise ValidationError(
            "Email already exists."
        )
    def validate_phone(self, field):

        user = User.query.filter_by(
        phone=field.data
    ).first()

        if user:

            raise ValidationError(
            "Phone number already exists."
        )