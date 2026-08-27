from flask import Blueprint, render_template,redirect, url_for, flash
from flask_login import login_required

from app.utils.decorators import admin_required
from app.models import User,db
from werkzeug.security import generate_password_hash
from app.forms import UserForm, EditUserForm
from flask_login import current_user



user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/users"
)


@user_bp.route("/")
@login_required
@admin_required
def users():

    users = User.query.all()

    return render_template(
        "users/users.html",
        users=users
    )
@user_bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():

    form = UserForm()

    if form.validate_on_submit():

        user = User(
            username=form.username.data,
            password_hash=generate_password_hash(
                form.password.data
            ),
            role=form.role.data,
            status=form.status.data
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "User created successfully.",
            "success"
        )

        return redirect(
            url_for("user.users")
        )

    return render_template(
        "users/add_user.html",
        form=form
    )
    
@user_bp.route(
    "/edit/<int:user_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_user(user_id):

    user = User.query.get_or_404(user_id)

    form = EditUserForm(obj=user)

    if form.validate_on_submit():

        try:

            user.username = form.username.data
            user.role = form.role.data
            user.status = form.status.data

            db.session.commit()

            flash(
                "User updated successfully.",
                "success"
            )

            return redirect(
                url_for("user.users")
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Error updating user: {str(e)}",
                "danger"
            )

    return render_template(
        "users/edit_user.html",
        form=form,
        user=user
    )




@user_bp.route("/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):

    try:

        user = User.query.get_or_404(user_id)

        if user.id == current_user.id:

            flash(
                "You cannot delete your own account.",
                "danger"
            )

            return redirect(
                url_for("user.users")
            )

        db.session.delete(user)
        db.session.commit()

        flash(
            "User deleted successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        flash(
            f"Error deleting user: {str(e)}",
            "danger"
        )

    return redirect(
        url_for("user.users")
    )