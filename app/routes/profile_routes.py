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
from app.forms import ChangePasswordForm,ProfileForm
from flask_login import logout_user
from app.models import db


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

         
            current_user.set_password(
                    form.new_password.data
                )
            

            from app.models import db

            db.session.commit()
            logout_user()

            flash(
                "Password changed successfully.Please log in",
                "success"
            )

            return redirect(
                url_for("auth.login")
            )

    return render_template(
        "profile/change_password.html",
        form=form
    )
@profile_bp.route(
    "/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_profile():

    form = ProfileForm(
        user_id=current_user.id,
        obj=current_user
    )

    if form.validate_on_submit():

        current_user.email = (
            form.email.data
        )

        current_user.phone = (
            form.phone.data
        )

       
        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "profile.my_profile"
            )
        )

    return render_template(
        "profile/edit_profile.html",
        form=form
    )