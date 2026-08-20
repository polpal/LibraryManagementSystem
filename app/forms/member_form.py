from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, Length,ValidationError

def validate_name_characters(form, field):
    for char in field.data:
        if not (
            char.isalpha()
            or char.isspace()
            or char in ".-'"
        ):
            raise ValidationError("Name contains invalid characters.")
        
def validate_phone(form, field):
    from ..models import Member

    phone = field.data.strip()

    member = Member.query.filter_by(phone=phone).first()

    if member and member.id != form.member_id:
        raise ValidationError(
            "This phone number is already registered."
        )
def validate_email(form, field):
    from ..models import Member

    email = field.data.strip().lower()

    member = Member.query.filter_by(email=email).first()

    if member and member.id != form.member_id:
        raise ValidationError(
            "This email address is already registered."
        )
class MemberForm(FlaskForm):
    
    def __init__(self, member_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member_id = member_id

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
            Length(min=2, max=150),
        validate_name_characters
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
           DataRequired(),
        Length(min=10, max=10),
        validate_phone
        ]
    )

    email = StringField(
        "Email",
        validators=[
           DataRequired(),
        Email(),
        Length(max=120),
        validate_email
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
    