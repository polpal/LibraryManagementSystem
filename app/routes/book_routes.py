from flask import Blueprint, render_template

from ..models import Book


book_bp = Blueprint("book", __name__)


@book_bp.route("/books")
def books():

    books = Book.query.all()

    return render_template(
        "books.html",
        books=books
    )