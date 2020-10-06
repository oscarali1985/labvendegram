"""empty message

Revision ID: cf906e7be049
Revises: 05ce472ab466
Create Date: 2020-10-06 00:09:44.322772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf906e7be049'
down_revision = '05ce472ab466'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('suscripcion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plan', sa.Enum('BASICO', name='planes'), nullable=False),
    sa.Column('fecha_registro', sa.Date(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('usuario', sa.Column('fecha_registro', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'fecha_registro')
    op.drop_table('suscripcion')
    # ### end Alembic commands ###
