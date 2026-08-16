from flask import Blueprint, render_template, request, redirect, url_for

from ..models import db, Member


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

    # Find the highest existing Member No.
    last_member = (
        Member.query
        .filter(Member.member_no.like("MEM%"))
        .order_by(Member.id.desc())
        .first()
    )

    if last_member:
        try:
            last_number = int(last_member.member_no[3:])
            next_number = last_number + 1
        except (ValueError, TypeError):
            next_number = 1
    else:
        next_number = 1

    next_member_no = f"MEM{next_number:03d}"

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        designation = request.form.get("designation", "").strip()
        department = request.form.get("department", "").strip()
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()

        # Required field validation
        if not name:
            return "Member name is required.", 400

        # Create member using the server-generated Member No.
        member = Member(
            member_no=next_member_no,
            name=name,
            designation=designation,
            department=department,
            address=address,
            phone=phone,
            email=email
        )

        db.session.add(member)
        db.session.commit()

        return redirect(url_for("member.members"))

    return render_template(
        "add_member.html",
        next_member_no=next_member_no
    )