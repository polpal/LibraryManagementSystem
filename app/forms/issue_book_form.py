from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class IssueBookForm(FlaskForm):

    member_id = SelectField("Member", validators=[DataRequired()], coerce=int)

    book_id = SelectField("Book", validators=[DataRequired()], coerce=int)

    submit = SubmitField("Issue Book")
