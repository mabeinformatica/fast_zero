"""table users

Revision ID: 5af9e5be0f81
Revises: 7d2f2a36edd4
Create Date: 2024-05-11 11:01:39.960458

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5af9e5be0f81'
down_revision: Union[str, None] = '7d2f2a36edd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'users',
        sa.Column('name', sa.String(100), nullable=False),
    )


def downgrade() -> None:
    pass
