from datetime import date

from app.models import db, Book, Member, Transaction
from app.utils.logger import logger


def issue_book_to_member(member_id, book_id, due_date):
    logger.info(
        f"Issue request received. "
        f"member_id={member_id}, "
        f"book_id={book_id}"
    )
    member = Member.query.get(member_id)

    if not member:
        logger.warning(
            f"Issue failed. Member not found. "
            f"member_id={member_id}"
        )
        return False, "Member not found."

    book = Book.query.get(book_id)

    if not book:
        logger.warning(
            f"Issue failed. Book not found. "
            f"book_id={book_id}"
        )
        return False, "Book not found."

    if book.status != "Available":
        logger.warning(
            f"Issue failed. Book is not available. "
            f"book_id={book_id}"
        )
        return False, "Book is not available."

    existing_transaction = Transaction.query.filter_by(
        member_id=member.id,
        return_date=None
    ).first()

    if existing_transaction:
        logger.warning(
        f"Issue failed. "
        f"Member already has an active transaction. "
        f"member_no={member.member_no}"
    )
        return False, "This member already has a book issued."

    last_transaction = Transaction.query.order_by(
    Transaction.transaction_no.desc()
).first()

    if last_transaction:
     transaction_no = last_transaction.transaction_no + 1
    else:
     transaction_no = 100001

    transaction = Transaction(
    transaction_no=transaction_no,
    book_id=book.id,
    member_id=member.id,
    issue_date=date.today(),
    due_date=due_date,
    transaction_type="Issue"
)

    book.status = "Issued"

    try:
        db.session.add(transaction)
        db.session.commit()
        logger.info(
    f"Book issued successfully. "
    f"transaction_no={transaction_no}, "
    f"member_no={member.member_no}, "
    f"accession_no={book.accession_no}"
)

    except Exception as e:

        db.session.rollback()

        logger.exception(
        "Error while issuing book"
        )
        return False, "Database error occurred."

    return True, "Book issued successfully."

def return_book(transaction_no):
    logger.info(
        f"Return request received. "
        f"transaction_no={transaction_no}"
    )
    transaction = Transaction.query.filter_by(
        transaction_no=transaction_no
    ).first()

    if not transaction:
        logger.warning(
            f"Return failed. "
            f"Transaction not found. "
            f"transaction_no={transaction_no}"
        )

        return False, "Transaction not found."

    if transaction.return_date is not None:
        logger.warning(
            f"Return failed. "
            f"Book already returned. "
            f"transaction_no={transaction_no}"
        )
        return False, "This book has already been returned."
    
    try:
        transaction.return_date = date.today()

        transaction.book.status = "Available"

        db.session.commit()
        logger.info(
            f"Book returned successfully. "
            f"transaction_no={transaction_no}, "
            f"member_no={transaction.member.member_no}, "
            f"accession_no={transaction.book.accession_no}"
        )
        return True, "Book returned successfully."
    except Exception:

            db.session.rollback()
            logger.exception(
            "Database error during return_book"
        )
    return False, "Database error occurred."

def reissue_book(transaction_no, due_date):

    previous_transaction = Transaction.query.filter_by(
        transaction_no=transaction_no
    ).first()

    if not previous_transaction:
        logger.warning(
            f"Reissue failed. "
            f"Transaction not found. "
            f"transaction_no={transaction_no}"
        )
        return False, "Previous transaction not found."

    if previous_transaction.return_date is None:
        logger.warning(
            f"Reissue failed. "
            f"Book not returned yet. "
            f"transaction_no={transaction_no}"
        )
        return False, "This book has not been returned yet."

    member = previous_transaction.member
    book = previous_transaction.book

    if not member:
        logger.warning(
            f"Reissue failed. Member not found. "
            f"transaction_no={transaction_no}"
        )
        return False, "Member not found."

    if not book:
        logger.warning(
            f"Reissue failed. Book not found. "
            f"transaction_no={transaction_no}"
        )
        return False, "Book not found."

    if book.status != "Available":
        logger.warning(
                    f"Reissue failed. Book not avaiable "
                    f"transaction_no={transaction_no}"
                )
        return False, "Book is not available."

    existing_transaction = Transaction.query.filter_by(
        member_id=member.id,
        return_date=None
    ).first()

    if existing_transaction:
        logger.warning(
                            f"Reissue failed. This member already has a book issued. "
                            f"transaction_no={transaction_no}"
                        )
        return False, "This member already has a book issued."

    last_transaction = Transaction.query.order_by(
        Transaction.transaction_no.desc()
    ).first()

    if last_transaction:
        transaction_no = last_transaction.transaction_no + 1
    else:
        transaction_no = 100001

    transaction = Transaction(
        transaction_no=transaction_no,
        book_id=book.id,
        member_id=member.id,
        issue_date=date.today(),
        due_date=due_date,
        transaction_type="Reissue"
    )

    book.status = "Issued"

    try:
        db.session.add(transaction)
        db.session.commit()
        logger.info(
            f"Book reissued successfully. "
            f"transaction_no={transaction_no}, "
            f"member_no={member.member_no}, "
            f"accession_no={book.accession_no}"
        )

        return True, "Book reissued successfully."

    except Exception:
        db.session.rollback()
        logger.exception(
            "Database error during reissue_book"
        )
        return False, "Database error occurred."