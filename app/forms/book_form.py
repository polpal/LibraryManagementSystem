from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError

from ..models import Book


def validate_accession_no(form, field):

    accession_no = field.data.strip()

    book = Book.query.filter_by(
        accession_no=accession_no
    ).first()

    if book and book.id != form.book_id:
        raise ValidationError(
            "This accession number already exists."
        )


class BookForm(FlaskForm):

    def __init__(self, book_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.book_id = book_id

    accession_no = StringField(
        "Accession No.",
        validators=[
            DataRequired(),
            Length(max=50),
            validate_accession_no
        ]
    )

    book_name = StringField(
        "Book Name",
        validators=[
            DataRequired(),
            Length(min=1, max=200)
        ]
    )

    author = StringField(
        "Author",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    category = StringField(
        "Category",
        validators=[
            Length(max=100)
        ]
    )