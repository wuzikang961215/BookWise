"""Add payment_intent_id to payments; remove booked_count from slots

Revision ID: 593789a95b74
Revises: c16d7a1c7d90
Create Date: 2025-06-29 20:06:42.845258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '593789a95b74'
down_revision: Union[str, None] = 'c16d7a1c7d90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('payment_intent_id', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'payments', ['payment_intent_id'])
    op.drop_column('slots', 'booked_count')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('slots', sa.Column('booked_count', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'payments', type_='unique')
    op.drop_column('payments', 'payment_intent_id')
    # ### end Alembic commands ###
