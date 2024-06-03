"""empty message

Revision ID: 10564c56521d
Revises: 
Create Date: 2024-01-15 18:14:03.589527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '10564c56521d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'user_type',
               existing_type=postgresql.ENUM('PENDING', 'INTRANSIT', 'DELIVERED', name='orderstatus'),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'user_type',
               existing_type=sa.String(),
               type_=postgresql.ENUM('PENDING', 'INTRANSIT', 'DELIVERED', name='orderstatus'),
               existing_nullable=True)
    # ### end Alembic commands ###
