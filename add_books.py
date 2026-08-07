import pandas as pd

from app import create_app, db
from app.models import Book


file_path = "Library.xlsx"

df = pd.read_excel(file_path)


app = create_app()


with app.app_context():

    for index, row in df.iterrows():

        book = Book(
            serial_no=row["serial_no"],
            accession_no=row["accession_no"],
            book_name=row["book_name"],
            author=row["author"],
            category=row["category"],
            status="Available"
        )

        db.session.add(book)

    db.session.commit()


print("Books imported successfully")