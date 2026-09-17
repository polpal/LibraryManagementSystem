from app import create_app, db
from app.models.transaction import Transaction
from app.models.member import Member
from app.models.user import User

app = create_app()

with app.app_context():

    print("Before Cleanup")
    print("Members:", Member.query.count())
    print("Transactions:", Transaction.query.count())
    print("Users:", User.query.count())

    # Delete transactions
    Transaction.query.delete()

    # Delete members
    Member.query.delete()

    # Delete member users only
    User.query.filter_by(role="Member").delete()

    db.session.commit()

    print("\nAfter Cleanup")
    print("Members:", Member.query.count())
    print("Transactions:", Transaction.query.count())
    print("Users:", User.query.count())

    print("\nCleanup Complete")
