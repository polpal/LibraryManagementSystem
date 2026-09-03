from flask import Blueprint

book_category_bp = Blueprint(
    "book_category",
    __name__,
    url_prefix="/categories"
)
from flask import render_template
from flask_login import login_required

from ..models import BookCategory, Book
from flask import render_template, redirect, url_for, flash
from ..forms.book_category_form import BookCategoryForm
from ..models import db

@book_category_bp.route("/")
@login_required
def list_categories():

    categories = BookCategory.query.order_by(
       BookCategory.id.asc()
    ).all()

    return render_template(
        "categories/categories.html",
        categories=categories
    )
    
@book_category_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_category():

    form = BookCategoryForm()

    if form.validate_on_submit():

        category = BookCategory(
            name=form.name.data.strip(),
            status=form.status.data
        )

        db.session.add(category)
        db.session.commit()

        flash(
            "Category added successfully.",
            "success"
        )

        return redirect(
            url_for("book_category.list_categories")
        )

    return render_template(
        "categories/add_category.html",
        form=form
    )
@book_category_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_category(id):

    category = BookCategory.query.get_or_404(id)

    form = BookCategoryForm(obj=category)

    if form.validate_on_submit():

        category.name = form.name.data.strip()
        category.status = form.status.data

        db.session.commit()

        flash(
            "Category updated successfully.",
            "success"
        )

        return redirect(
            url_for("book_category.list_categories")
        )

    return render_template(
        "categories/edit_category.html",
        form=form,
        category=category
    )
@book_category_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_category(id):

    category = BookCategory.query.get_or_404(id)

    # Check whether this category is being used by any book
    books_using_category = Book.query.filter_by(
        category=category.name
    ).first()

    if books_using_category:
        flash(
            "This category is currently being used by a book and cannot be deleted.",
            "danger"
        )

        return redirect(
            url_for("book_category.list_categories")
        )

    db.session.delete(category)
    db.session.commit()

    flash(
        "Category deleted successfully.",
        "success"
    )

    return redirect(
        url_for("book_category.list_categories")
    )