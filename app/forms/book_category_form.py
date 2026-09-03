from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length

from ..models import BookCategory


class BookCategoryForm(FlaskForm):

    name = StringField(
        "Category Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive")
        ]
    )