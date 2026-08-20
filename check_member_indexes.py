import sqlite3

from app import create_app
from app.models import db


app = create_app()

with app.app_context():

    db_path = db.engine.url.database

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    indexes = cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'index'
        AND tbl_name = 'member'
    """).fetchall()

    connection.close()

    print("\nMember indexes:")

    for index in indexes:
        print(index[0])