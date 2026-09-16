from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
import secrets
import string

from app.models import member
from app.models import user
from app.models.user import User
from app.utils.decorators import role_required

from ..models import db, Member, Transaction
from ..forms.member_form import MemberForm
from app.utils.logger import logger
from app.utils.email import send_member_welcome_email

member_bp = Blueprint("member", __name__)


@member_bp.route("/members")
@login_required
def members():

    members = Member.query.all()

    return render_template("members.html", members=members)


@member_bp.route("/members/add", methods=["GET", "POST"])
@login_required
@role_required("Admin", "Librarian")
def add_member():

    # Find all existing MEM member numbers
    members = Member.query.filter(Member.member_no.like("MEM%")).all()

    numbers = []

    for member in members:
        try:
            number = int(member.member_no[3:])
            numbers.append(number)
        except (ValueError, TypeError):
            pass

    if numbers:
        next_number = max(numbers) + 1
    else:
        next_number = 1

    next_member_no = f"MEM{next_number:03d}"

    # Create Flask-WTF form
    form = MemberForm()

    # Server-generated Member No.
    form.member_no.data = next_member_no

    if form.validate_on_submit():

        try:
            # Create User account for the Member
            characters = string.ascii_letters + string.digits + "!@#$%"
            temporary_password = "".join(secrets.choice(characters) for _ in range(12))

            user = User(
                username=next_member_no,
                role="Member",
                status=form.status.data,
                email=form.email.data.strip().lower(),
                phone=form.phone.data.strip(),
                must_change_password=True,
            )

            user.set_password(temporary_password)

            db.session.add(user)

            # Get the generated User ID
            db.session.flush()

            # Create Member linked to User
            member = Member(
                member_no=next_member_no,
                name=form.name.data.strip(),
                designation=form.designation.data.strip(),
                department=form.department.data.strip(),
                address=form.address.data.strip(),
                phone=form.phone.data.strip(),
                email=form.email.data.strip().lower(),
                status=form.status.data,
                user_id=user.id,
            )

            db.session.add(member)

            # Save User + Member together
            db.session.commit()

            logger.info(
                f"Member created. "
                f"member_no={member.member_no}, "
                f"name={member.name}, "
                f"user_id={user.id}"
            )

            # Send welcome email separately
            try:
                send_member_welcome_email(member, temporary_password)

                logger.info(f"Welcome email sent successfully to {member.email}")

                flash(
                    "Member and login account created successfully. "
                    "Welcome email sent.",
                    "success",
                )

            except Exception:
                logger.exception(
                    f"Member created, but welcome email failed for {member.email}"
                )

                flash(
                    "Member and login account created successfully, "
                    "but the welcome email could not be sent.",
                    "warning",
                )

        except Exception:
            db.session.rollback()

            logger.exception("Database error during add_member")

            flash("Unable to create member.", "danger")

        return redirect(url_for("member.members"))
    return render_template("add_member.html", form=form, next_member_no=next_member_no)


@member_bp.route("/members/edit/<int:member_id>", methods=["GET", "POST"])
@login_required
def edit_member(member_id):

    member = Member.query.get_or_404(member_id)

    form = MemberForm(member_id=member.id, obj=member)

    if form.validate_on_submit():

        member.name = form.name.data.strip()
        member.designation = form.designation.data.strip()
        member.department = form.department.data.strip()
        member.address = form.address.data.strip()
        member.phone = form.phone.data.strip()
        member.email = form.email.data.strip().lower()
        member.status = form.status.data

        # Update linked User account
        if member.user:
            member.user.phone = form.phone.data.strip()
            member.user.email = form.email.data.strip().lower()
            member.user.status = form.status.data

        db.session.commit()

        flash("Member updated successfully.", "success")

        return redirect(url_for("member.members"))

    return render_template("edit_member.html", form=form, member=member)


@member_bp.route("/members/delete/<int:member_id>", methods=["POST"])
@login_required
def delete_member(member_id):

    member = Member.query.get_or_404(member_id)

    transaction = Transaction.query.filter_by(member_id=member.id).first()

    if transaction:
        flash("This member has transaction history and cannot be deleted.", "danger")
        return redirect(url_for("member.members"))

    user = member.user

    try:
        # Delete Member
        db.session.delete(member)

        # Delete linked User account
        if user:
            db.session.delete(user)

        db.session.commit()

        flash("Member and login account deleted successfully.", "success")

    except Exception:
        db.session.rollback()

        logger.exception(f"Error deleting member {member.member_no}")

        flash("Unable to delete member.", "danger")

    return redirect(url_for("member.members"))


@member_bp.route("/my-books")
@login_required
def my_books():

    if current_user.role != "Member":
        abort(403)

    transactions = (
        Transaction.query.filter(Transaction.member_id == current_user.member.id)
        .order_by(Transaction.id.desc())
        .all()
    )

    return render_template("my_books.html", transactions=transactions)
