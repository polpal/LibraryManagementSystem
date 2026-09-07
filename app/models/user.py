from flask_login import UserMixin

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from itsdangerous import URLSafeTimedSerializer



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
    
    email = db.Column(
    db.String(120),
    unique=True,
    nullable=False
    )

    phone = db.Column(
    db.String(20),
    unique=True,
    nullable=False
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
    def get_reset_token(self):

        serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

        return serializer.dumps(
        self.email,
        salt="password-reset-salt"
    )
@staticmethod
def verify_reset_token(
    token,
    expiration=3600
):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:
        email = serializer.loads(
            token,
            salt="password-reset-salt",
            max_age=expiration
        )

    except Exception:
        return None

    return User.query.filter_by(
        email=email
    ).first()