# app/models/role_menu.py

from . import db


class RoleMenu(db.Model):

    __tablename__ = "role_menus"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    role_name = db.Column(
        db.String(50),
        nullable=False
    )

    menu_id = db.Column(
        db.Integer,
        db.ForeignKey("menus.id"),
        nullable=False
    )

    menu = db.relationship(
        "Menu",
        backref="role_menus"
    )

    def __repr__(self):

        return f"<RoleMenu {self.role_name}>"