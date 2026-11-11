from datetime import date

from app import create_app
from app.models import Transaction
from app.services.report_service import (
    get_issued_books_report,
    get_overdue_books_report,
    get_report_summary,
)


def main():
    app = create_app()

    with app.app_context():

        # Get report data.
        issued_books = get_issued_books_report()
        overdue_books = get_overdue_books_report()
        summary = get_report_summary()

        issued_ids = {transaction.transaction_no for transaction in issued_books}

        # Check that overdue records belong to issued records.
        assert all(
            transaction.transaction_no in issued_ids for transaction in overdue_books
        ), "Overdue report contains a transaction missing from issued report."

        # Check that every issued book is still unreturned.
        assert all(
            transaction.return_date is None for transaction in issued_books
        ), "Issued report contains a returned book."

        # Check that every overdue book is unreturned and past its due date.
        assert all(
            transaction.return_date is None and transaction.due_date < date.today()
            for transaction in overdue_books
        ), "Overdue report contains an invalid transaction."

        # Check summary counts.
        assert summary["total_issued"] == len(
            issued_books
        ), "Summary issued count does not match issued report."

        assert summary["total_overdue"] == len(
            overdue_books
        ), "Summary overdue count does not match overdue report."

        # Independently verify today's issue count.
        expected_issued_today = Transaction.query.filter(
            Transaction.issue_date == date.today()
        ).count()

        assert (
            summary["issued_today"] == expected_issued_today
        ), "Summary issued-today count is incorrect."

        print("All report service tests passed!")
        print(f"Currently issued books: {summary['total_issued']}")
        print(f"Overdue books: {summary['total_overdue']}")
        print(f"Books issued today: {summary['issued_today']}")


if __name__ == "__main__":
    main()
