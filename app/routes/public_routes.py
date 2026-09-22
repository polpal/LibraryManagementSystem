from flask import Blueprint, render_template

from app.models import Book

public_bp = Blueprint("public", __name__)


@public_bp.route("/books")
def books():

    books = Book.query.all()

    return render_template("public_books.html", books=books)
