from flask import Blueprint, render_template, redirect, url_for,flash

from ..models import db, Member,Transaction
from ..forms.member_form import MemberForm


member_bp = Blueprint("member", __name__)


@member_bp.route("/members")
def members():

    members = Member.query.all()

    return render_template(
        "members.html",
        members=members
    )


@member_bp.route("/members/add", methods=["GET", "POST"])
def add_member():

    # Find all existing MEM member numbers
    members = (
        Member.query
        .filter(Member.member_no.like("MEM%"))
        .all()
    )

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

        member = Member(
            member_no=next_member_no,
            name=form.name.data.strip(),
            designation=form.designation.data.strip(),
            department=form.department.data.strip(),
            address=form.address.data.strip(),
            phone=form.phone.data.strip(),
            email=form.email.data.strip(),
            status=form.status.data
        )

        db.session.add(member)
        db.session.commit()

        flash("Member created successfully.", "success")
        return redirect(url_for("member.members"))

    return render_template(
        "add_member.html",
        form=form,
        next_member_no=next_member_no
    )
    
@member_bp.route("/members/edit/<int:member_id>", methods=["GET", "POST"])
def edit_member(member_id):

    member = Member.query.get_or_404(member_id)

    form = MemberForm(member_id=member.id, obj=member)

    if form.validate_on_submit():

        member.name = form.name.data.strip()
        member.designation = form.designation.data.strip()
        member.department = form.department.data.strip()
        member.address = form.address.data.strip()
        member.phone = form.phone.data.strip()
        member.email = form.email.data.strip()
        member.status = form.status.data

        db.session.commit()

        flash("Member updated successfully.", "success")

        return redirect(url_for("member.members"))

    return render_template(
        "edit_member.html",
        form=form,
        member=member
    )
    
@member_bp.route("/members/delete/<int:member_id>", methods=["POST"])
def delete_member(member_id):

    member = Member.query.get_or_404(member_id)

    transaction = Transaction.query.filter_by(
        member_id=member.id
    ).first()

    if transaction:
        flash(
            "This member has transaction history and cannot be deleted.",
            "danger"
        )
        return redirect(url_for("member.members"))

    db.session.delete(member)
    db.session.commit()

    flash(
        "Member deleted successfully.",
        "success"
    )

    return redirect(url_for("member.members"))