from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime, date, timedelta
from app.forms import IssueBookForm
from app.forms.reissue_form import ReissueForm

from ..models import Book, Member, Transaction
from app.services.settings_service import get_int_setting
from ..services.transaction_service import (
    issue_book_to_member,
    return_book,
    reissue_book,
)

transaction_bp = Blueprint("transaction", __name__)


@transaction_bp.route("/issued-books")
@login_required
def issued_books():

    transactions = Transaction.query.filter_by(return_date=None).all()

    return render_template("issued_books.html", transactions=transactions)


@transaction_bp.route("/transactions")
@login_required
def transactions():

    transactions = Transaction.query.order_by(Transaction.transaction_no.desc()).all()

    active_member_ids = {
        transaction.member_id
        for transaction in transactions
        if transaction.return_date is None
    }

    return render_template(
        "transactions.html",
        transactions=transactions,
        active_member_ids=active_member_ids,
    )


@transaction_bp.route("/issue", methods=["GET", "POST"])
@login_required
def issue_book():

    form = IssueBookForm()

    books = Book.query.filter_by(status="Available").all()

    members = Member.query.filter_by(status="Active").all()

    form.member_id.choices = [
        (member.id, f"{member.member_no} - {member.name}") for member in members
    ]

    form.book_id.choices = [
        (book.id, f"{book.accession_no} - {book.book_name}") for book in books
    ]

    if form.validate_on_submit():

        success, message = issue_book_to_member(form.member_id.data, form.book_id.data)

        if success:
            flash(message, "success")

            return redirect(url_for("transaction.issued_books"))

        flash(message, "danger")
    loan_days = get_int_setting("LOAN_DAYS", 30)

    due_date = date.today() + timedelta(days=loan_days)
    return render_template(
        "issue_book.html", form=form, today=date.today(), due_date=due_date
    )


@transaction_bp.route("/return/<int:transaction_no>")
@login_required
def return_book_route(transaction_no):

    success, message = return_book(transaction_no)

    if not success:
        return message, 400

    return redirect(url_for("transaction.issued_books"))


@transaction_bp.route("/reissue/<int:transaction_no>", methods=["GET", "POST"])
@login_required
def reissue_book_route(transaction_no):

    transaction = Transaction.query.filter_by(transaction_no=transaction_no).first()

    if not transaction:
        return "Transaction not found.", 404

    if transaction.return_date is not None:
        flash("Only active issued books can be renewed.", "danger")
        return redirect(url_for("transaction.issued_books"))

    form = ReissueForm()

    if form.validate_on_submit():

        success, message = reissue_book(transaction_no)

        if not success:
            flash(message, "danger")
            return redirect(url_for("transaction.issued_books"))

        flash(message, "success")

        return redirect(url_for("transaction.issued_books"))

    today = date.today()

    loan_days = get_int_setting("REISSUE_LOAN_DAYS", 30)

    due_date = today + timedelta(days=loan_days)

    return render_template(
        "reissue_book.html",
        transaction=transaction,
        form=form,
        today=today,
        due_date=due_date,
    )
