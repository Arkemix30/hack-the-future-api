"""add location field

Revision ID: ec8e461cdd82
Revises: 0b223aad73a2
Create Date: 2023-04-01 14:45:51.881333

"""
import sqlalchemy as sa

# import geoalchemy2          # POSTGIS
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "ec8e461cdd82"
down_revision = "0b223aad73a2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "CREATE TYPE energylocation AS ENUM ('LOCAL', 'OFICINAS_ADMINISTRATIVAS', 'PLANTA_DE_ENVASADO', 'DESCONOCIDO');"
    )
    # Change energy_type to energy_category
    op.execute(
        "CREATE TYPE energycategory AS ENUM ('CONSUMO_ADMINISTRATIVO', 'CONSUMO_LOGISTICO', 'CONSUMO_DE_DISTIBUCION');"
    )
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "energy",
        sa.Column(
            "location",
            sa.Enum(
                "LOCAL",
                "OFICINAS_ADMINISTRATIVAS",
                "PLANTA_DE_ENVASADO",
                "DESCONOCIDO",
                name="energylocation",
            ),
            nullable=True,
        ),
    )
    op.add_column(
        "energy",
        sa.Column(
            "energy_category",
            sa.Enum(
                "CONSUMO_ADMINISTRATIVO",
                "CONSUMO_LOGISTICO",
                "CONSUMO_DE_DISTIBUCION",
                name="energycategory",
            ),
            nullable=True,
        ),
    )
    op.drop_column("energy", "energy_type")
    # ### end Alembic commands ###


def downgrade() -> None:
    op.execute("DROP TYPE energylocation;")
    op.execute("DROP TYPE energycategory;")
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "energy",
        sa.Column(
            "energy_type",
            postgresql.ENUM(
                "CONSUMO_ADMINISTRATIVO",
                "CONSUMO_LOGISTICO",
                "CONSUMO_DE_DISTIBUCION",
                name="energytype",
            ),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("energy", "energy_category")
    op.drop_column("energy", "location")
    # ### end Alembic commands ###
