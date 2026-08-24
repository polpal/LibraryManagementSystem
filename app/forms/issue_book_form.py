from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired


class IssueBookForm(FlaskForm):

    member_id = SelectField(
        "Member",
        validators=[DataRequired()],
        coerce=int
    )

    book_id = SelectField(
        "Book",
        validators=[DataRequired()],
        coerce=int
    )

    due_date = DateField(
        "Due Date",
        validators=[DataRequired()],
        format="%Y-%m-%d"
    )

    submit = SubmitField(
        "Issue Book"
    )