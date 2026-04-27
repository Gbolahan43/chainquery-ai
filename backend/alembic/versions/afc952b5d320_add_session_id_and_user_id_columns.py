"""Add session_id and user_id columns

Revision ID: afc952b5d320
Revises: bf65eb265dbf
Create Date: 2026-01-28 21:04:57.787296

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'afc952b5d320'
down_revision = 'bf65eb265dbf'
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
