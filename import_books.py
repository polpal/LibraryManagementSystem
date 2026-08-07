import pandas as pd

from app import create_app, db
from app.models import Book


file_path = "library.xlsx"

df = pd.read_excel(file_path)
df.columns = (
    df.columns
    .str.replace(r'[\t\n\r]', '', regex=True)
    .str.strip()
)
print(df.columns.tolist())

app = create_app()


with app.app_context():

    imported = 0
    skipped = 0

    for index, row in df.iterrows():

        existing_book = Book.query.filter_by(
            accession_no=row["accession_no"]
        ).first()

        if existing_book:
            skipped += 1
            continue


        book = Book(
            serial_no=row["serial_no"],
            accession_no=row["accession_no"],
            book_name=row["book_name"],
            author=row["author"],
            category=row["category"],
            status="Available"
        )

        db.session.add(book)

        imported += 1


    db.session.commit()

    print(f"Imported: {imported}")
    print(f"Skipped: {skipped}")