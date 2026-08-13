import pandas as pd

from app import create_app
from app.models import db, Member


EXCEL_FILE = "library.xlsx"


app = create_app()

with app.app_context():

    df = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Members"
    )

    for _, row in df.iterrows():

        member_no = str(row["member_no"])

        existing_member = Member.query.filter_by(
            member_no=member_no
        ).first()

        if existing_member:
            print(f"Member {member_no} already exists. Skipping.")
            continue

        member = Member(
            member_no=member_no,
            name=row["name"],
            designation=row["designation"],
            department=row["department"],
            address=row["address"],
            phone=str(row["phone"]),
            email=row["email"],
            status=row["status"]
        )

        db.session.add(member)

    db.session.commit()

    print("Members imported successfully.")