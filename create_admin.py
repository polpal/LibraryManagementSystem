from werkzeug.security import generate_password_hash

from app import create_app
from app.models import db, User


app = create_app()

with app.app_context():

    existing_user = User.query.filter_by(
        username="admin"
    ).first()

    if existing_user:
        print("Admin user already exists.")

    else:

        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="Admin",
            email='admin@library.com',
            phone='9999999999'
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully.")