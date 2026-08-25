from flask import Blueprint, flash, render_template

from app.forms.admin_form import AdminLoginForm
from app.models.admin import Admin
from werkzeug.security import check_password_hash


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    form = AdminLoginForm()

    if form.validate_on_submit():

        admin = Admin.query.filter_by(
            username=form.username.data
        ).first()

        if not admin:
            flash("Invalid username", "danger")

        elif not check_password_hash(
            admin.password,
            form.password.data
            ):
             flash("Invalid password", "danger")
        else:
            flash("Login successful", "success")

    return render_template(
        "admin/login.html",
        form=form
    )