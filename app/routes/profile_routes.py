from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for
)

from werkzeug.security import generate_password_hash
from app.forms import ChangePasswordForm


profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


@profile_bp.route("/")
@login_required
def my_profile():
    return render_template(
        "profile/profile.html",
        user=current_user
    )
    
@profile_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
def change_password():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not current_user.check_password(
            form.current_password.data
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

        else:

            current_user.password_hash = (
                current_user.set_password(
                    form.new_password.data
                )
            )

            from app.models import db

            db.session.commit()

            flash(
                "Password changed successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "profile.my_profile"
                )
            )

    return render_template(
        "profile/change_password.html",
        form=form
    )