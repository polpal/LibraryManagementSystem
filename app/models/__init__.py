from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .book import Book
from .member import Member
from .transaction import Transaction
from .user import User
from .admin import Admin