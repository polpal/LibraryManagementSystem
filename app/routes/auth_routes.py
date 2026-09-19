from flask import Blueprint, render_template, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user
from ..forms.login_form import LoginForm
from ..models import User
from werkzeug.security import check_password_hash
from ..forms.forgot_password_form import ForgotPasswordForm
from ..forms.reset_password_form import ResetPasswordForm
from ..utils.email import send_reset_email
from flask import request

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if not user:

            flash("Invalid username", "danger")
        elif user.status != "Active":

            flash("Your account is inactive.", "danger")

        elif not user.check_password(form.password.data):

            flash("Invalid password", "danger")

        else:
            print("LOGIN SUCCESSFUL")
            from flask import session

            login_user(user)
            session.permanent = True

            if user.must_change_password:
                flash("You must change your password before continuing.", "warning")
                return redirect(url_for("auth.change_password"))

            flash("Login successful", "success")

            return redirect(url_for("dashboard.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    print("forgot_password route hit")

    form = ForgotPasswordForm()

    print("Request method:", request.method)

    if form.validate_on_submit():

        print("Form validated")

        user = User.query.filter_by(username=form.username.data,email=form.email.data).first()

        print("Username entered:", form.username.data)
        print("Email entered:", form.email.data)

        if user:
            print("User found:", user.email)
            send_reset_email(user)

        flash("If the account details are valid, a reset link has been sent.", "info")

        return redirect(url_for("auth.login"))

    else:
        if request.method == "POST":
            print("Form errors:", form.errors)

    return render_template("auth/forgot_password.html", form=form)


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    user = User.verify_reset_token(token)

    if not user:

        flash("Invalid or expired reset link.", "danger")

        return redirect(url_for("auth.login"))

    form = ResetPasswordForm()

    if form.validate_on_submit():

        user.set_password(form.password.data)

        from ..models import db

        db.session.commit()

        flash("Password reset successful. Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", form=form)


@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    form = ResetPasswordForm()

    if form.validate_on_submit():

        current_user.set_password(form.password.data)
        current_user.must_change_password = False

        from ..models import db

        db.session.commit()

        flash("Password changed successfully.", "success")

        return redirect(url_for("dashboard.dashboard"))

    return render_template("auth/reset_password.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))
