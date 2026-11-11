from datetime import date

from app import create_app
from app.services.report_service import (
    get_issued_books_report,
    get_overdue_books_report,
)


def main():
    app = create_app()

    with app.app_context():
        issued_books = get_issued_books_report()
        overdue_books = get_overdue_books_report()
        issued_ids = {transaction.transaction_no for transaction in issued_books}

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

        print("Report service tests passed!")
        print(f"Currently issued books: {len(issued_books)}")
        print(f"Overdue books: {len(overdue_books)}")


if __name__ == "__main__":
    main()
