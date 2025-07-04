"""Use Enum for payment method

Revision ID: c16d7a1c7d90
Revises: 211bd09454a3
Create Date: 2025-06-27 16:25:55.536710

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c16d7a1c7d90'
down_revision: Union[str, None] = '211bd09454a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ✅ Step 1: Manually create PostgreSQL enum type
    op.execute(
        "CREATE TYPE paymentmethod AS ENUM ('credit_card', 'paypal', 'alipay', 'wechat_pay', 'apple_pay')"
    )

    # ✅ Step 2: Alter column to use this new enum
    op.alter_column('payments', 'method',
        existing_type=sa.VARCHAR(),
        type_=sa.Enum('credit_card', 'paypal', 'alipay', 'wechat_pay', 'apple_pay', name='paymentmethod'),
        nullable=False,
        postgresql_using='method::text::paymentmethod'
    )


def downgrade() -> None:
    # ✅ Step 1: Revert column back to VARCHAR
    op.alter_column('payments', 'method',
        existing_type=sa.Enum('credit_card', 'paypal', 'alipay', 'wechat_pay', 'apple_pay', name='paymentmethod'),
        type_=sa.VARCHAR(),
        nullable=True
    )

    # ✅ Step 2: Drop the enum type
    op.execute("DROP TYPE paymentmethod")
