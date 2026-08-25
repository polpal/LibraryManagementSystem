from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import login_user,logout_user

from ..forms.login_form import LoginForm
from ..models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if not user:

            flash(
                "Invalid username",
                "danger"
            )

        elif not check_password_hash(
            user.password_hash,
            form.password.data
        ):

            flash(
                "Invalid password",
                "danger"
            )

        else:
            print("LOGIN SUCCESSFUL")
            login_user(user)

            flash(
                "Login successful",
                "success"
            )

            return redirect(
                url_for("dashboard.dashboard")
            )

    return render_template(
        "auth/login.html",
        form=form
    )
    
@auth_bp.route("/logout")
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )