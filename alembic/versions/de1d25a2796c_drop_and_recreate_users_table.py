"""Drop and recreate users table

Revision ID: de1d25a2796c
Revises: 7fbbbfe398ee
Create Date: 2024-11-10 17:16:45.690384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de1d25a2796c'
down_revision = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop the foreign key constraint from rentals to users
    op.drop_constraint('rentals_user_id_fkey', 'rentals', type_='foreignkey')
    
    # Drop the existing users table
    op.drop_table('users')

    # Recreate the users table with the new schema
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('password_hash', sa.String, nullable=False),
        sa.Column('age', sa.Integer, nullable=False),
        sa.Column('license_number', sa.String, nullable=False, unique=True)
    )

    # Re-add the foreign key constraint to the rentals table
    op.create_foreign_key(
        'rentals_user_id_fkey', 'rentals', 'users', ['user_id'], ['user_id']
    )

def downgrade():
    # Drop the foreign key constraint
    op.drop_constraint('rentals_user_id_fkey', 'rentals', type_='foreignkey')

    # Drop the new users table
    op.drop_table('users')

    # Recreate the old users table (if necessary)
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('age', sa.Integer, nullable=False),
        sa.Column('license_number', sa.String, nullable=False, unique=True)
    )

    # Re-add the original foreign key constraint to rentals
    op.create_foreign_key(
        'rentals_user_id_fkey', 'rentals', 'users', ['user_id'], ['user_id']
    )
