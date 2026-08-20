from app import create_app
from app.models import db, Member


app = create_app()


with app.app_context():

    phones = (
        db.session.query(
            Member.phone,
            db.func.count(Member.phone)
        )
        .group_by(Member.phone)
        .having(db.func.count(Member.phone) > 1)
        .all()
    )

    emails = (
        db.session.query(
            Member.email,
            db.func.count(Member.email)
        )
        .group_by(Member.email)
        .having(db.func.count(Member.email) > 1)
        .all()
    )

    print("\nDuplicate phones:")
    if phones:
        for phone, count in phones:
            print(f"{phone} → {count} records")
    else:
        print("None")

    print("\nDuplicate emails:")
    if emails:
        for email, count in emails:
            print(f"{email} → {count} records")
    else:
        print("None")