from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime, date

from .models import Book, Member, Transaction
from .services.transaction_service import (
    issue_book_to_member,
    return_book,
    reissue_book
)
main = Blueprint("main", __name__)


@main.route("/")
def index():

    books = Book.query.all()

    return render_template(
        "index.html",
        books=books
    )


@main.route("/books")
def books():

    books = Book.query.all()

    return render_template(
        "books.html",
        books=books
    )

@main.route("/issued-books")
def issued_books():

    transactions = Transaction.query.filter_by(
        return_date=None
    ).all()

    return render_template(
        "issued_books.html",
        transactions=transactions
    )

@main.route("/transactions")
def transactions():

    transactions = Transaction.query.order_by(
        Transaction.transaction_no.desc()
    ).all()

    active_member_ids = {
        transaction.member_id
        for transaction in transactions
        if transaction.return_date is None
    }

    return render_template(
        "transactions.html",
        transactions=transactions,
        active_member_ids=active_member_ids
    )

@main.route("/issue", methods=["GET", "POST"])
def issue_book():

    if request.method == "GET":

        books = Book.query.filter_by(status="Available").all()
        members = Member.query.filter_by(status="Active").all()
        today = date.today()

        return render_template(
            "issue_book.html",
            books=books,
            members=members,
            today=today
        )
    if request.method == "POST":

        member_id = request.form.get("member_id")
        book_id = request.form.get("book_id")
        due_date = request.form.get("due_date")

    if not member_id:
        return "Please select a member.", 400

    if not book_id:
        return "Please select a book.", 400

    if not due_date:
        return "Please select a due date.", 400

    due_date = datetime.strptime(
        due_date,
        "%Y-%m-%d"
    ).date()

    success, message = issue_book_to_member(
        member_id,
        book_id,
        due_date
    )

    if not success:
        return message, 400

    return redirect(url_for("main.issued_books"))

@main.route("/return/<int:transaction_no>")
def return_book_route(transaction_no):

    success, message = return_book(transaction_no)

    if not success:
        return message, 400

    return redirect(url_for("main.issued_books"))

@main.route("/reissue/<int:transaction_no>", methods=["GET", "POST"])
def reissue_book_route(transaction_no):

    transaction = Transaction.query.filter_by(
        transaction_no=transaction_no
    ).first()

    if not transaction:
        return "Transaction not found.", 404

    if transaction.return_date is None:
        return "This book has not been returned yet.", 400

    if request.method == "GET":

        today = date.today()

        return render_template(
            "reissue_book.html",
            transaction=transaction,
            today=today
        )

    due_date = request.form.get("due_date")

    if not due_date:
        return "Please select a due date.", 400

    due_date = datetime.strptime(
        due_date,
        "%Y-%m-%d"
    ).date()

    success, message = reissue_book(
        transaction_no,
        due_date
    )

    if not success:
        return message, 400

    return redirect(url_for("main.issued_books"))