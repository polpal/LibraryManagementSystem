from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import admin_required
from app.models import Book, Member, Transaction, User
from datetime import date
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def dashboard():
    today = date.today()
    if current_user.role == "Member":
        my_issued_books = Transaction.query.filter(
            Transaction.member_id == current_user.member.id,
            Transaction.return_date.is_(None),
        ).count()

        my_overdue_books = Transaction.query.filter(
            Transaction.member_id == current_user.member.id,
            Transaction.return_date.is_(None),
            Transaction.due_date < today,
        ).count()

        recent_transactions = (
            Transaction.query.filter(Transaction.member_id == current_user.member.id)
            .order_by(Transaction.id.desc())
            .limit(5)
            .all()
        )

        return render_template(
            "dashboard/dashboard.html",
            is_member=True,
            my_issued_books=my_issued_books,
            my_overdue_books=my_overdue_books,
            recent_transactions=recent_transactions,
        )

    overdue_books = Transaction.query.filter(
        Transaction.due_date < today, Transaction.return_date.is_(None)
    ).count()

    total_books = Book.query.count()

    available_books = Book.query.filter_by(status="Available").count()

    issued_books = Book.query.filter_by(status="Issued").count()

    total_members = Member.query.count()

    active_members = Member.query.filter_by(status="Active").count()
    total_users = User.query.count()

    recent_transactions = (
        Transaction.query.order_by(Transaction.id.desc()).limit(5).all()
    )

    return render_template(
        "dashboard/dashboard.html",
        is_member=False,
        total_books=total_books,
        available_books=available_books,
        issued_books=issued_books,
        total_members=total_members,
        overdue_books=overdue_books,
        active_members=active_members,
        total_users=total_users,
        recent_transactions=recent_transactions,
    )


@dashboard_bp.route("/admin-test")
@login_required
@admin_required
def admin_test():

    return "Admin Access Granted"
