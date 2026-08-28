from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    ValidationError
)

from app.models import User

class EditUserForm(FlaskForm):
    
    def __init__(self, user_id=None, *args, **kwargs):

     super().__init__(*args, **kwargs)

     self.user_id = user_id

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("Admin", "Admin"),
            ("Librarian", "Librarian")
        ],
        validators=[
            DataRequired()
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive")
        ],
        validators=[
            DataRequired()
        ]
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
        "Update User"
    )
    
def validate_username(self, field):

    user = User.query.filter_by(
        username=field.data
    ).first()

    if user and user.id != self.user_id:

        raise ValidationError(
            "Username already exists."
        )
        
def validate_email(self, field):

    user = User.query.filter_by(
        email=field.data
    ).first()

    if user and user.id != self.user_id:

        raise ValidationError(
            "Email already exists."
        )
def validate_phone(self, field):

    user = User.query.filter_by(
        phone=field.data
    ).first()

    if user and user.id != self.user_id:

        raise ValidationError(
            "Phone number already exists."
        )