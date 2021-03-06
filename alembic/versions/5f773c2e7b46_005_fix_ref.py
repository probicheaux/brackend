"""005/fix-ref.

Revision ID: 5f773c2e7b46
Revises: 8d7ed542163c
Create Date: 2021-12-23 11:55:05.310266
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5f773c2e7b46"
down_revision = "8d7ed542163c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("rounds_bracket_fkey", "rounds", type_="foreignkey")
    op.create_foreign_key(None, "rounds", "brackets", ["bracket"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "rounds", type_="foreignkey")
    op.create_foreign_key("rounds_bracket_fkey", "rounds", "tournaments", ["bracket"], ["id"])
    # ### end Alembic commands ###
