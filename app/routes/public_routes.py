from flask import Blueprint, render_template, request
from sqlalchemy import or_

from app.models import Book, BookCategory

public_bp = Blueprint("public", __name__)


@public_bp.route("/public-books")
def public_books():

    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Book.query

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                Book.book_name.ilike(search_term),
                Book.author.ilike(search_term),
                Book.publisher.ilike(search_term),
                Book.category.has(BookCategory.name.ilike(search_term)),
            )
        )

    books = query.order_by(Book.book_name).paginate(
        page=page,
        per_page=10,
        error_out=False,
    )
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template(
            "includes/public_books_results.html",
            books=books,
            search=search,
        )
    return render_template(
        "public_books.html",
        books=books,
        search=search,
    )
