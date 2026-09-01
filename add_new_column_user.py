from app.models import db

db.session.execute(
    db.text(
        "ALTER TABLE user ADD COLUMN email VARCHAR(120)"
    )
)

db.session.execute(
    db.text(
        "ALTER TABLE user ADD COLUMN phone VARCHAR(20)"
    )
)

db.session.commit()