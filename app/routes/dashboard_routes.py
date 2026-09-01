from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import admin_required
from app.models import Book, Member, Transaction,User
from datetime import date


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def dashboard():
    
    today = date.today()

    overdue_books = Transaction.query.filter(
    Transaction.due_date < today,
    Transaction.return_date.is_(None)
    ).count()

    total_books = Book.query.count()

    available_books = Book.query.filter_by(
        status="Available"
    ).count()

    issued_books = Book.query.filter_by(
        status="Issued"
    ).count()

    total_members = Member.query.count()
    
    active_members = Member.query.filter_by(
    status="Active"
    ).count()
    total_users = User.query.count()
    
    recent_transactions = Transaction.query.order_by(
    Transaction.id.desc()
).limit(5).all()

    return render_template(
        "dashboard/dashboard.html",
        total_books=total_books,
        available_books=available_books,
        issued_books=issued_books,
        total_members=total_members,
        overdue_books=overdue_books,
        active_members=active_members,
        total_users=total_users,
        recent_transactions=recent_transactions
    )
    

@dashboard_bp.route("/admin-test")
@login_required
@admin_required
def admin_test():

    return "Admin Access Granted"