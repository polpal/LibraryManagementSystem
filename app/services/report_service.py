from datetime import date

from app.models import Transaction


def get_issued_books_report():
    """Return all transactions for books that have not been returned."""

    return (
        Transaction.query.filter(Transaction.return_date.is_(None))
        .order_by(Transaction.due_date.asc())
        .all()
    )


def get_overdue_books_report():
    """Return active transactions whose due date has passed."""

    today = date.today()

    return (
        Transaction.query.filter(
            Transaction.return_date.is_(None),
            Transaction.due_date < today,
        )
        .order_by(Transaction.due_date.asc())
        .all()
    )
