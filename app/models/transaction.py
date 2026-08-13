from . import db


class Transaction(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    transaction_no = db.Column(
        db.Integer,
        unique=True,
        nullable=False
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("book.id"),
        nullable=False
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("member.id"),
        nullable=False
    )

    book = db.relationship(
        "Book",
        backref="transactions"
    )

    member = db.relationship(
        "Member",
        backref="transactions"
    )

    issue_date = db.Column(
        db.Date,
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=False
    )

    return_date = db.Column(
        db.Date,
        nullable=True
    )

    transaction_type = db.Column(
        db.String(20),
        nullable=False
    )