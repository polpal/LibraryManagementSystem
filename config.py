from datetime import timedelta
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "library-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "library.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=30
    )
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = "partho.sarkar.cosh@gmail.com"
    MAIL_PASSWORD = "lmjqmzrdwpamtbtg"

    MAIL_DEFAULT_SENDER = "partho.sarkar.cosh@gmail.com"