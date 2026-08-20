import sqlite3

from app import create_app
from app.models import db


app = create_app()

with app.app_context():

    db_path = db.engine.url.database

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        uq_member_phone
        ON member (phone)
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        uq_member_email
        ON member (email)
    """)

    connection.commit()
    connection.close()

    print("Unique indexes created successfully.")