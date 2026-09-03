from .import db


class BookCategory(db.Model):

    __tablename__ = "book_categories"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Active"
    )

    def __repr__(self):
        return f"<BookCategory {self.name}>"