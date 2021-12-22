"""004/enumify.

Revision ID: 8d7ed542163c
Revises: d79bb9d29e57
Create Date: 2021-12-22 16:50:51.825350
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "8d7ed542163c"
down_revision = "d79bb9d29e57"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    userrole = postgresql.ENUM("player", "spectator", "organizer", name="userrole")
    userrole.create(op.get_bind())
    op.alter_column("brackets", "tournament", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("match_users", "match", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("match_users", "user", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("match_users", "score", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("matches", "round", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("matches", "round_position", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column(
        "matches",
        "progress",
        existing_type=postgresql.ENUM(
            "not_started", "in_progress", "completed", name="progressenum"
        ),
        nullable=False,
    )
    op.alter_column("rounds", "name", existing_type=sa.VARCHAR(length=255), nullable=False)
    op.alter_column("rounds", "bracket", existing_type=sa.INTEGER(), nullable=True)
    op.add_column(
        "user_tournaments",
        sa.Column(
            "role",
            postgresql.ENUM("player", "spectator", "organizer", name="userrole"),
            nullable=False,
        ),
    )
    op.alter_column("user_tournaments", "user_id", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("user_tournaments", "tournament_id", existing_type=sa.INTEGER(), nullable=True)
    op.drop_column("user_tournaments", "is_organizer")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_tournaments",
        sa.Column("is_organizer", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.alter_column("user_tournaments", "tournament_id", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("user_tournaments", "user_id", existing_type=sa.INTEGER(), nullable=False)
    op.drop_column("user_tournaments", "role")
    op.alter_column("rounds", "bracket", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("rounds", "name", existing_type=sa.VARCHAR(length=255), nullable=True)
    op.alter_column(
        "matches",
        "progress",
        existing_type=postgresql.ENUM(
            "not_started", "in_progress", "completed", name="progressenum"
        ),
        nullable=True,
    )
    op.alter_column("matches", "round_position", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("matches", "round", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("match_users", "score", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("match_users", "user", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("match_users", "match", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("brackets", "tournament", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###
