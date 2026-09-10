from . import db


class Member(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    member_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    designation = db.Column(
        db.String(100)
    )

    department = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.String(300)
    )

    phone = db.Column(
        db.String(20), unique=True, nullable=False
    )

    email = db.Column(
        db.String(120), unique=True, nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=True,
        nullable=True
)

    user = db.relationship(
         "User",
         back_populates="member"
)


    def __repr__(self):
     return f"<Member {self.member_no} - {self.name}>"