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


def get_report_summary():
    """Return summary counts for the library reports."""

    today = date.today()

    total_issued = Transaction.query.filter(Transaction.return_date.is_(None)).count()

    total_overdue = Transaction.query.filter(
        Transaction.return_date.is_(None),
        Transaction.due_date < today,
    ).count()

    issued_today = Transaction.query.filter(Transaction.issue_date == today).count()

    return {
        "total_issued": total_issued,
        "total_overdue": total_overdue,
        "issued_today": issued_today,
    }


def get_filtered_report(report_type, start_date, end_date):
    """Return report transactions filtered by report type and date range."""

    query = Transaction.query

    if report_type == "issued":

        query = query.filter(
            Transaction.return_date.is_(None),
            Transaction.issue_date >= start_date,
            Transaction.issue_date <= end_date,
        )

        query = query.order_by(Transaction.issue_date.desc())

    elif report_type == "overdue":

        today = date.today()

        query = query.filter(
            Transaction.return_date.is_(None),
            Transaction.due_date < today,
            Transaction.due_date >= start_date,
            Transaction.due_date <= end_date,
        )

        query = query.order_by(Transaction.due_date.asc())

    elif report_type == "returned":

        query = query.filter(
            Transaction.return_date.isnot(None),
            Transaction.return_date >= start_date,
            Transaction.return_date <= end_date,
        )

        query = query.order_by(Transaction.return_date.desc())

    elif report_type == "history":

        query = query.filter(
            Transaction.issue_date >= start_date,
            Transaction.issue_date <= end_date,
        )

        query = query.order_by(Transaction.issue_date.desc())

    else:
        raise ValueError("Invalid report type.")

    return query.all()
