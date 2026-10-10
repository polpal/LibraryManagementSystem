
from decimal import Decimal

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, current_user
from app.utils.decorators import role_required

from app.forms.settings_form import SettingsForm
from app.services.settings_service import (
    get_int_setting,
    get_setting,
    save_settings,
)
from app.utils.logger import logger


settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/", methods=["GET", "POST"])
@login_required
@role_required("Admin", "Librarian")
def settings_page():

    form = SettingsForm()

    # Save settings when the form is submitted.
    if form.validate_on_submit():

        settings = {
            "LOAN_DAYS": form.loan_days.data,
            "REISSUE_LOAN_DAYS": form.reissue_loan_days.data,
            "MAX_BOOKS_PER_MEMBER": form.max_books_per_member.data,
            "MAX_REISSUE_COUNT": form.max_reissue_count.data,
            "FINE_PER_DAY": form.fine_per_day.data,
        }

        try:
            save_settings(settings)
            flash("Settings saved successfully.", "success")
            return redirect(url_for("settings.settings_page"))

        except Exception:
            logger.exception("Failed to save system settings.")
            flash("Unable to save settings. Please try again.", "danger")

    # Load existing settings when the page is opened.
    elif request.method == "GET":

        form.loan_days.data = get_int_setting("LOAN_DAYS", 30)

        form.reissue_loan_days.data = get_int_setting(
            "REISSUE_LOAN_DAYS", 30
        )

        # Default 1 preserves the current one-active-book restriction.
        form.max_books_per_member.data = get_int_setting(
            "MAX_BOOKS_PER_MEMBER", 1
        )

        form.max_reissue_count.data = get_int_setting(
            "MAX_REISSUE_COUNT", 2
        )

        form.fine_per_day.data = Decimal(
            str(get_setting("FINE_PER_DAY", "1"))
        )

    return render_template("settings.html", form=form)
