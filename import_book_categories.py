
import pandas as pd

from app import create_app, db
from app.models import BookCategory


file_path = "library.xlsx"

df = pd.read_excel(file_path)

# Clean Excel column names
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

    # Get unique categories from Excel
    categories = (
        df["category"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    for category_name in categories:

        # Check if category already exists
        existing_category = BookCategory.query.filter_by(
            name=category_name
        ).first()

        if existing_category:
            skipped += 1
            continue

        # Create new category
        category = BookCategory(
            name=category_name,
            status="Active"
        )

        db.session.add(category)
        imported += 1

    db.session.commit()

    print(f"Imported categories: {imported}")
    print(f"Skipped categories: {skipped}")

