from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .book import Book
from .member import Member
from .transaction import Transaction
from .user import User
from .admin import Admin
from .book_category import BookCategory
from .menu import Menu
from .role_menu import RoleMenu
from .system_setting import SystemSetting
