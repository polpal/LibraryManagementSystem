from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    ValidationError
)

from app.models import User


class ProfileForm(FlaskForm):

    def __init__(
        self,
        user_id=None,
        *args,
        **kwargs
    ):
        super().__init__(
            *args,
            **kwargs
        )

        self.user_id = user_id

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
        "Update Profile"
    )

    def validate_email(
        self,
        field
    ):

        user = User.query.filter_by(
            email=field.data
        ).first()

        if (
            user and
            user.id != self.user_id
        ):
            raise ValidationError(
                "Email already exists."
            )

    def validate_phone(
        self,
        field
    ):

        user = User.query.filter_by(
            phone=field.data
        ).first()

        if (
            user and
            user.id != self.user_id
        ):
            raise ValidationError(
                "Phone number already exists."
            )