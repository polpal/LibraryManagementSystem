from flask import Blueprint, render_template

from app.models import (
    Book,
    Member,
    Transaction
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():

    total_books = Book.query.count()

    total_members = Member.query.count()

    issued_books = Transaction.query.filter_by(
    return_date=None
    ).count()

    return render_template(
    "index.html",
    total_books=total_books,
    total_members=total_members,
    issued_books=issued_books
)

@main_bp.app_errorhandler(403)
def forbidden(error):

    return render_template(
        "errors/403.html"
    ), 403