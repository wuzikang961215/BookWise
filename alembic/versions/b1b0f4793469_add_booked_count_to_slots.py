"""add booked_count to slots

Revision ID: b1b0f4793469
Revises: 7e5354f7c659
Create Date: 2025-06-25 15:31:29.250571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1b0f4793469'
down_revision: Union[str, None] = '7e5354f7c659'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column("slots", sa.Column("booked_count", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("slots", "booked_count")
