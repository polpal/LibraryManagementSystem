from . import db


class Book(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    accession_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    serial_no = db.Column(
        db.String(50)
    )
    book_name = db.Column(
        db.String(200),
        nullable=False
    )

    author = db.Column(
        db.String(150)
    )

    category = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(20),
        default="Available"
    )