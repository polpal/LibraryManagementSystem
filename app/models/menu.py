# app/models/menu.py

from . import db


class Menu(db.Model):

    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)

    menu_name = db.Column(db.String(100), nullable=False, unique=True)

    endpoint = db.Column(db.String(100), nullable=False)
    active_prefix = db.Column(db.String(100), nullable=True)
    icon = db.Column(db.String(100), nullable=True)

    display_order = db.Column(db.Integer, default=0)

    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):

        return f"<Menu {self.menu_name}>"
