from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length
)


class EditUserForm(FlaskForm):

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

    submit = SubmitField(
        "Update User"
    )