from flask import Blueprint, render_template, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user
from ..forms.login_form import LoginForm
from ..models import User
from werkzeug.security import check_password_hash
from ..forms.forgot_password_form import ForgotPasswordForm
from ..forms.reset_password_form import ResetPasswordForm
from ..utils.email import send_reset_email
from flask import request
from flask import session

from ..forms.confirm_login_form import ConfirmLoginForm

from ..utils.session_manager import (
    generate_session_token,
    activate_session,
    invalidate_session,
)
import time

from ..utils.session_manager import is_session_valid

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

            # Check whether this browser already owns the session.
            if (
                current_user.is_authenticated
                and current_user.id == user.id
                and is_session_valid(user, session.get("active_session_token"))
            ):
                return redirect(url_for("dashboard.dashboard"))

            # An existing token requires confirmation.
            if user.active_session_token:

                session["pending_login_user_id"] = user.id
                session["pending_login_created_at"] = time.time()

                return redirect(url_for("auth.confirm_login"))

            # No existing session: activate a new session.
            token = generate_session_token()

            activate_session(user, token)

            login_user(user)
            session.permanent = True
            session["active_session_token"] = token

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

        user = User.query.filter_by(
            username=form.username.data, email=form.email.data
        ).first()

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


@auth_bp.route("/confirm-login", methods=["GET", "POST"])
def confirm_login():

    form = ConfirmLoginForm()

    pending_user_id = session.get("pending_login_user_id")
    pending_created_at = session.get("pending_login_created_at")

    # Check whether a pending login exists.
    if not pending_user_id or not pending_created_at:

        flash("No pending login request found.", "warning")
        return redirect(url_for("auth.login"))

    # Pending confirmation expires after 5 minutes.
    if time.time() - pending_created_at > 300:

        session.pop("pending_login_user_id", None)
        session.pop("pending_login_created_at", None)

        flash("Login confirmation expired. Please login again.", "warning")
        return redirect(url_for("auth.login"))

    if form.validate_on_submit():

        # User cancelled the takeover.
        if form.cancel.data:

            session.pop("pending_login_user_id", None)
            session.pop("pending_login_created_at", None)

            flash("Login cancelled. Existing session remains active.", "info")

            return redirect(url_for("auth.login"))

        if form.confirm.data:

            user = User.query.get(pending_user_id)

            if not user or user.status != "Active":

                session.pop("pending_login_user_id", None)
                session.pop("pending_login_created_at", None)

                flash("Account is unavailable. Please login again.", "danger")
                return redirect(url_for("auth.login"))

            # Generate and activate the new session.
            token = generate_session_token()

            activate_session(user, token)

            session.pop("pending_login_user_id", None)
            session.pop("pending_login_created_at", None)

            login_user(user)

            session.permanent = True
            session["active_session_token"] = token

            if user.must_change_password:

                flash("You must change your password before continuing.", "warning")

                return redirect(url_for("auth.change_password"))

            flash("Previous session terminated. Login successful.", "success")

            return redirect(url_for("dashboard.dashboard"))

    return render_template("auth/confirm_login.html", form=form)
