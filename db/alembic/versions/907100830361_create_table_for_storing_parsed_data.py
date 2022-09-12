"""create table for storing parsed data

Revision ID: 907100830361
Revises: 
Create Date: 2022-09-10 16:08:56.450083

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '907100830361'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "parsed_data",
        sa.Column("ad_link", sa.String(250)),
        sa.Column("image_url", sa.String(250)),
        sa.Column("title", sa.String(250)),
        sa.Column("currency", sa.String(15)),
        sa.Column("city", sa.String(50)),
        sa.Column("description", sa.Text),
        sa.Column("bedrooms", sa.String),
        sa.Column("date", sa.String(10)),
        sa.Column("price", sa.String(15)),
    )


def downgrade() -> None:
    op.drop_table("parsed_data")
