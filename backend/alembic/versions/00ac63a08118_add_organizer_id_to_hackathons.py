"""add organizer_id to hackathons

Revision ID: 00ac63a08118
Revises: 00ac63a08117
Create Date: 2026-09-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00ac63a08118'
down_revision: Union[str, None] = '00ac63a08117'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('hackathons', schema=None) as batch_op:
        batch_op.add_column(sa.Column('organizer_id', sa.String(), nullable=True))
        batch_op.create_index(batch_op.f('ix_hackathons_organizer_id'), ['organizer_id'], unique=False)
        batch_op.create_foreign_key('fk_hackathons_organizer_id', 'users', ['organizer_id'], ['id'])


def downgrade() -> None:
    with op.batch_alter_table('hackathons', schema=None) as batch_op:
        batch_op.drop_constraint('fk_hackathons_organizer_id', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_hackathons_organizer_id'))
        batch_op.drop_column('organizer_id')
