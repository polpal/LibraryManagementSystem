
import pandas as pd

from app import create_app, db
from app.models import Book, BookCategory


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

        # Check whether book already exists
        existing_book = Book.query.filter_by(
            accession_no=row["accession_no"]
        ).first()

        if existing_book:
            skipped += 1
            continue

        # Get category name from Excel
        category_name = str(row["category"]).strip()

        # Find existing category
        category = BookCategory.query.filter_by(
            name=category_name
        ).first()

        # Create category if it does not exist
        if not category:
            category = BookCategory(
                name=category_name,
                status="Active"
            )

            db.session.add(category)
            db.session.flush()

        # Create book
        book = Book(
            serial_no=row["serial_no"],
            accession_no=row["accession_no"],
            book_name=row["book_name"],
            author=row["author"],
            category=category,
            status="Available"
        )

        db.session.add(book)
        imported += 1

    db.session.commit()

    print(f"Imported: {imported}")
    print(f"Skipped: {skipped}")


