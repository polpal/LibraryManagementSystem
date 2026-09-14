from flask_wtf import FlaskForm
from wtforms import SubmitField


class ReissueForm(FlaskForm):

    submit = SubmitField("Reissue Book")
