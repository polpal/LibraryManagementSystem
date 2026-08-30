from werkzeug.security import generate_password_hash

from app import create_app
from app.models import db, User


app = create_app()

with app.app_context():

    existing_user = User.query.filter_by(
        username="librarian"
    ).first()

    if existing_user:
        print("Librarian already exists.")

    else:

        librarian = User(
            username="librarian",
            password_hash=generate_password_hash("lib123"),
            role="Librarian",
            email='librarian@library.com',
            phone='8888888888'
        )

        db.session.add(librarian)
        db.session.commit()

        print("Librarian created successfully.")