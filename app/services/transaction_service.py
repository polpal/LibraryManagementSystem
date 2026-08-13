from datetime import date

from app.models import db, Book, Member, Transaction


def issue_book_to_member(member_id, book_id, due_date):

    member = Member.query.get(member_id)

    if not member:
        return False, "Member not found."

    book = Book.query.get(book_id)

    if not book:
        return False, "Book not found."

    if book.status != "Available":
        return False, "Book is not available."

    existing_transaction = Transaction.query.filter_by(
        member_id=member.id,
        return_date=None
    ).first()

    if existing_transaction:
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

    db.session.add(transaction)
    db.session.commit()

    return True, "Book issued successfully."

def return_book(transaction_no):

    transaction = Transaction.query.filter_by(
        transaction_no=transaction_no
    ).first()

    if not transaction:
        return False, "Transaction not found."

    if transaction.return_date is not None:
        return False, "This book has already been returned."

    transaction.return_date = date.today()

    transaction.book.status = "Available"

    db.session.commit()

    return True, "Book returned successfully."