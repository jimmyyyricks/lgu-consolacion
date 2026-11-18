"""Add featured story metadata to public content."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20261027_featured_public_content"
down_revision: Union[str, None] = "3578b437f586"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "public_content",
        sa.Column("image_url", sa.String(length=1000), nullable=True),
    )
    op.add_column(
        "public_content",
        sa.Column(
            "featured",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    op.drop_column("public_content", "featured")
    op.drop_column("public_content", "image_url")
