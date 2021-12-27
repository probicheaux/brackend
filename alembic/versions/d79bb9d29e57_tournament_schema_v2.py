"""tournament_schema v2

Revision ID: d79bb9d29e57
Revises: 32d58879aac1
Create Date: 2021-12-22 15:30:48.704215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd79bb9d29e57'
down_revision = '32d58879aac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('brackets', 'tournament',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('match_users', 'match',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('match_users', 'user',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('match_users', 'score',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('matches', 'round',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('matches', 'round_position',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('rounds', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('rounds', 'bracket',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user_tournaments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user_tournaments', 'tournament_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_tournaments', 'tournament_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('user_tournaments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('rounds', 'bracket',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('rounds', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('matches', 'round_position',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('matches', 'round',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('match_users', 'score',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('match_users', 'user',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('match_users', 'match',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('brackets', 'tournament',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###