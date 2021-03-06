"""tournament_schema

Revision ID: 32d58879aac1
Revises: de23d4edb0e2
Create Date: 2021-12-22 12:18:17.123919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32d58879aac1'
down_revision = 'de23d4edb0e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brackets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('tournament', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tournament'], ['tournaments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rounds',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('bracket', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bracket'], ['tournaments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('round', sa.Integer(), nullable=True),
    sa.Column('round_position', sa.Integer(), nullable=True),
    sa.Column('progress', sa.Enum('not_started', 'in_progress', 'completed', name='progressenum'), nullable=True),
    sa.ForeignKeyConstraint(['round'], ['rounds.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('match_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('match', sa.Integer(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['match'], ['matches.id'], ),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('tournaments', sa.Column('date', sa.DateTime(), nullable=True))
    op.add_column('user_tournaments', sa.Column('is_organizer', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    op.drop_column('user_tournaments', 'is_organizer')
    op.drop_column('tournaments', 'date')
    op.drop_table('match_users')
    op.drop_table('matches')
    op.drop_table('rounds')
    op.drop_table('brackets')
    # ### end Alembic commands ###
