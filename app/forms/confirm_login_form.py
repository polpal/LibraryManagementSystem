from flask_wtf import FlaskForm
from wtforms import SubmitField


class ConfirmLoginForm(FlaskForm):

    confirm = SubmitField("Yes, Terminate Previous Session & Continue")

    cancel = SubmitField("Cancel")
