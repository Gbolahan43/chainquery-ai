"""actually add session_id and user_id columns

Revision ID: d2e3f4g5h6i7
Revises: afc952b5d320
Create Date: 2026-04-27 10:25:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'd2e3f4g5h6i7'
down_revision = 'afc952b5d320'
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('full_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Add columns to user_queries
    op.add_column('user_queries', sa.Column('session_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('user_queries', sa.Column('user_id', sa.Uuid(), nullable=True))
    
    op.create_index(op.f('ix_user_queries_session_id'), 'user_queries', ['session_id'], unique=False)
    op.create_foreign_key(None, 'user_queries', 'users', ['user_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'user_queries', type_='foreignkey')
    op.drop_index(op.f('ix_user_queries_session_id'), table_name='user_queries')
    op.drop_column('user_queries', 'user_id')
    op.drop_column('user_queries', 'session_id')
    
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
