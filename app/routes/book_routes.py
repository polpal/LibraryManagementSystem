from flask import Blueprint, render_template, request, redirect, url_for, flash

from ..models import Book, BookCategory
from .. import db
from ..forms.book_form import BookForm
from flask_login import login_required

book_bp = Blueprint("book", __name__)


@book_bp.route("/books")
@login_required
def books():

    books = Book.query.all()

    return render_template(
        "books.html",
        books=books
    )
    
 
@book_bp.route("/add-book", methods=["GET", "POST"])
@login_required
def add_book():

    if request.method == "POST":

        accession_no = request.form.get("accession_no")
        book_name = request.form.get("book_name")
        author = request.form.get("author")
        publisher = request.form.get("publisher")
        category_id = request.form.get("category_id")
        existing_book = Book.query.filter_by(
            accession_no=accession_no
        ).first()

        if existing_book:
            flash("Accession Number already exists.", "danger")
            return redirect(url_for("book.add_book"))

        new_book = Book(
            accession_no=accession_no,
            book_name=book_name,
            author=author,
            publisher=publisher,
           category_id=category_id,
            status="Available"
        )

        db.session.add(new_book)
        db.session.commit()

        flash("Book added successfully.", "success")

        return redirect(url_for("book.books"))
    categories = BookCategory.query.filter_by(status="Active"
).all()
    return render_template(
    "add_book.html",
    categories=categories
)   

@book_bp.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_book(book_id):

    book = Book.query.get_or_404(book_id)

    form = BookForm(
        book_id=book.id,
        obj=book
    )
    form.category_id.choices = [
    (category.id, category.name)
    for category in BookCategory.query.filter_by(status="Active").all()
]
    if form.validate_on_submit():

        book.accession_no = form.accession_no.data.strip()
        book.book_name = form.book_name.data.strip()
        book.author = form.author.data.strip()
        book.category_id = form.category_id.data
        book.publisher = form.publisher.data.strip()

        db.session.commit()

        flash(
            "Book updated successfully.",
            "success"
        )

        return redirect(
            url_for("book.books")
        )

    return render_template(
        "edit_book.html",
        form=form,
        book=book
    )