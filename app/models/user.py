from flask_login import UserMixin

from . import db
from werkzeug.security import generate_password_hash, check_password_hash




class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="Librarian"
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Active"
    )
    def __repr__(self):
     return f"<User {self.username}>"
 
    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(
        self.password_hash,
        password
        )