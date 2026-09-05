"""Convert book category to foreign key

Revision ID: 33acf07e5939
Revises: 06f4a6fa6afd
Create Date: 2026-09-04
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "33acf07e5939"
down_revision = "06f4a6fa6afd"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("book", schema=None) as batch_op:

        # Add category_id temporarily as nullable
        batch_op.add_column(
            sa.Column(
                "category_id",
                sa.Integer(),
                nullable=True
            )
        )

        # Create foreign key
        batch_op.create_foreign_key(
            "fk_book_category_id",
            "book_categories",
            ["category_id"],
            ["id"]
        )

        # Remove old text category
        batch_op.drop_column("category")


def downgrade():
    with op.batch_alter_table("book", schema=None) as batch_op:

        # Restore old category column
        batch_op.add_column(
            sa.Column(
                "category",
                sa.String(length=100),
                nullable=True
            )
        )

        # Remove foreign key
        batch_op.drop_constraint(
            "fk_book_category_id",
            type_="foreignkey"
        )

        # Remove category_id
        batch_op.drop_column("category_id")