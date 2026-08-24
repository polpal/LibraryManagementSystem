from flask import Blueprint, render_template, request, redirect, url_for,flash
from datetime import datetime, date
from app.forms import IssueBookForm

from ..models import Book, Member, Transaction
from ..services.transaction_service import (
    issue_book_to_member,
    return_book,
    reissue_book
)


transaction_bp = Blueprint("transaction", __name__)


@transaction_bp.route("/issued-books")
def issued_books():

    transactions = Transaction.query.filter_by(
        return_date=None
    ).all()

    return render_template(
        "issued_books.html",
        transactions=transactions
    )


@transaction_bp.route("/transactions")
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


@transaction_bp.route("/issue", methods=["GET", "POST"])
def issue_book():

    form = IssueBookForm()

    books = Book.query.filter_by(
        status="Available"
    ).all()

    members = Member.query.filter_by(
        status="Active"
    ).all()

    form.member_id.choices = [
        (
            member.id,
            f"{member.member_no} - {member.name}"
        )
        for member in members
    ]

    form.book_id.choices = [
        (
            book.id,
            f"{book.accession_no} - {book.book_name}"
        )
        for book in books
    ]

    if form.validate_on_submit():

        success, message = issue_book_to_member(
            form.member_id.data,
            form.book_id.data,
            form.due_date.data
        )

        if success:
            flash(message, "success")

            return redirect(
                url_for("transaction.issued_books")
            )

        flash(message, "danger")

    return render_template(
        "issue_book.html",
        form=form,
        today=date.today()
    )


@transaction_bp.route("/return/<int:transaction_no>")
def return_book_route(transaction_no):

    success, message = return_book(
        transaction_no
    )

    if not success:
        return message, 400

    return redirect(
        url_for("transaction.issued_books")
    )


@transaction_bp.route(
    "/reissue/<int:transaction_no>",
    methods=["GET", "POST"]
)
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

    return redirect(
        url_for("transaction.issued_books")
    )