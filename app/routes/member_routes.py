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

    if request.method == "POST":

        member_no = request.form["member_no"].strip()
        name = request.form["name"].strip()
        designation = request.form["designation"].strip()
        department = request.form["department"].strip()
        address = request.form["address"].strip()
        phone = request.form["phone"].strip()
        email = request.form["email"].strip()

        existing_member = Member.query.filter_by(
            member_no=member_no
        ).first()

        if existing_member:
            return "Member number already exists.", 400

        member = Member(
            member_no=member_no,
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

    return render_template("add_member.html")