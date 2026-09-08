from flask import Blueprint, render_template, request
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
import os
import uuid

from flask import current_app

from werkzeug.utils import secure_filename


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
        user_id=current_user.id       
    )
    if request.method == "GET":

        form.email.data = current_user.email
        form.phone.data = current_user.phone
    if form.validate_on_submit():

        try:

            current_user.email = form.email.data
            current_user.phone = form.phone.data
            print("PROFILE PICTURE DATA:", form.profile_picture.data)
            print("TYPE:", type(form.profile_picture.data))
            # Profile picture
            if form.profile_picture.data:

                file = form.profile_picture.data

                # Keep old picture name
                old_picture = current_user.profile_picture

                # Create unique filename
                original_filename = secure_filename(
                                    file.filename
                                )

                extension = os.path.splitext(
                        original_filename
                        )[1]

                filename = str(uuid.uuid4()) + extension

             # Upload folder
                upload_folder = os.path.join(
                                current_app.root_path,
                                "static",
                                "uploads",
                                "profile_pics"
                                )

             # Save new picture
                file.save(
                    os.path.join(
                            upload_folder,
                            filename
                        )
                    )

             # Update database
                current_user.profile_picture = filename

             # Delete old picture
                if old_picture:

                 old_file = os.path.join(
                        upload_folder,
                        old_picture
                    )

                 if os.path.exists(old_file):
                    os.remove(old_file)

            db.session.commit()

            flash(
                "Profile updated successfully.",
                "success"
            )

            return redirect(
                url_for("profile.my_profile")
            )

        except Exception as e:

            db.session.rollback()

            flash(
                "An error occurred while updating your profile.",
                "danger"
            )

            print(
                "PROFILE UPDATE ERROR:",
                e
            )

    return render_template(
        "profile/edit_profile.html",
        form=form
    )