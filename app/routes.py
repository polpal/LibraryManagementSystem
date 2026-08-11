from flask import Blueprint, render_template
from .models import Book

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

    books = Book.query.filter_by(status="Issued").all()

    return render_template(
        "issued_books.html",
        books=books
    )