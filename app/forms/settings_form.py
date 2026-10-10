from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class SettingsForm(FlaskForm):

    loan_days = IntegerField(
        "Loan Duration (Days)",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Loan duration must be at least 1 day."),
        ],
    )

    reissue_loan_days = IntegerField(
        "Reissue Duration (Days)",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Reissue duration must be at least 1 day."),
        ],
    )

    max_books_per_member = IntegerField(
        "Maximum Books Per Member",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Allow at least 1 book per member."),
        ],
    )

    max_reissue_count = IntegerField(
        "Maximum Reissue Count",
        validators=[
            DataRequired(),
            NumberRange(min=0, message="Reissue count cannot be negative."),
        ],
    )

    fine_per_day = DecimalField(
        "Fine Per Day",
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=0, message="Fine cannot be negative."),
        ],
    )

    submit = SubmitField("Save Settings")
