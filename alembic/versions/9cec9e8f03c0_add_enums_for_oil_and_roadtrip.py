"""add_enums_for_oil_and_roadtrip

Revision ID: 9cec9e8f03c0
Revises: ec8e461cdd82
Create Date: 2023-04-01 16:00:12.422286

"""
import sqlalchemy as sa

from alembic import op

# import geoalchemy2          # POSTGIS


# revision identifiers, used by Alembic.
revision = "9cec9e8f03c0"
down_revision = "ec8e461cdd82"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("oil", "oil_type")
    op.execute("DROP TYPE IF EXISTS oiltype;")
    op.execute("CREATE TYPE oiltype AS ENUM ('REFRIGERANTE','ACEITE');")
    op.execute(
        "CREATE TYPE oilcategory AS ENUM ('CONSUMO_ADMINISTRATIVO', 'CONSUMO_LOGISTICO', 'CONSUMO_DE_OPERACION');"
    )
    op.execute(
        "CREATE TYPE roadtripgrouptype AS ENUM ('EQUIPO_DE_VENTAS', 'EQUIPO_ADMINISTRATIVO');"
    )

    op.add_column(
        "oil",
        sa.Column(
            "oil_category",
            sa.Enum(
                "CONSUMO_ADMINISTRATIVO",
                "CONSUMO_LOGISTICO",
                "CONSUMO_DE_OPERACION",
                name="oilcategory",
            ),
            nullable=True,
        ),
    )
    op.add_column(
        "oil",
        sa.Column(
            "oil_type",
            sa.Enum("REFRIGERANTE", "ACEITE", name="oiltype"),
            nullable=True,
        ),
    )
    op.add_column(
        "roadtrip",
        sa.Column(
            "group",
            sa.Enum(
                "EQUIPO_DE_VENTAS",
                "EQUIPO_ADMINISTRATIVO",
                name="roadtripgrouptype",
            ),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TYPE IF EXISTS oiltype;")
    op.execute("DROP TYPE IF EXISTS oilcategory;")
    op.execute("DROP TYPE IF EXISTS roadtripgrouptype;")
    op.execute(
        "CREATE TYPE oiltype AS ENUM ('CONSUMO_ADMINISTRATIVO', 'CONSUMO_LOGISTICO', 'CONSUMO_DE_OPERACION');"
    )

    op.drop_column("roadtrip", "group")
    op.drop_column("oil", "oil_category")
    op.add_column(
        "oil",
        sa.Column(
            "oil_type",
            sa.Enum(
                "CONSUMO_ADMINISTRATIVO",
                "CONSUMO_LOGISTICO",
                "CONSUMO_DE_OPERACION",
                name="oiltype",
            ),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###
