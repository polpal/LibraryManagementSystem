from flask import Blueprint, render_template, request, redirect, url_for

from ..models import db, Member
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
            email=form.email.data.strip()
        )

        db.session.add(member)
        db.session.commit()

        return redirect(url_for("member.members"))

    return render_template(
        "add_member.html",
        form=form,
        next_member_no=next_member_no
    )