from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, Length


class MemberForm(FlaskForm):

    member_no = StringField(
        "Member No.",
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    designation = StringField(
        "Designation",
        validators=[
            Length(max=100)
        ]
    )

    department = StringField(
        "Department",
        validators=[
            Length(max=100)
        ]
    )

    address = StringField(
        "Address",
        validators=[
            Length(max=300)
        ]
    )

    phone = StringField(
        "Phone",
        validators=[
            Length(max=10)
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

    