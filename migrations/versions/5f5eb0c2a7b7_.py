"""empty message

Revision ID: 5f5eb0c2a7b7
Revises: 
Create Date: 2020-09-30 23:10:04.817549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f5eb0c2a7b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=100), nullable=False),
    sa.Column('foto', sa.String(length=200), nullable=False),
    sa.Column('descripcion', sa.String(length=2000), nullable=False),
    sa.Column('precio', sa.Float(precision=10), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.Column('etiqueta_uno', sa.Enum('ALIMENTOS', 'BEBIDAS', 'SALSAS', 'ENLATADOS', 'REFRESCOS', 'JUGOS', 'CEREALES', name='etiqueta'), nullable=False),
    sa.Column('etiqueta_dos', sa.Enum('ALIMENTOS', 'BEBIDAS', 'SALSAS', 'ENLATADOS', 'REFRESCOS', 'JUGOS', 'CEREALES', name='etiqueta'), nullable=True),
    sa.Column('etiqueta_tres', sa.Enum('ALIMENTOS', 'BEBIDAS', 'SALSAS', 'ENLATADOS', 'REFRESCOS', 'JUGOS', 'CEREALES', name='etiqueta'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('apellido', sa.String(length=50), nullable=False),
    sa.Column('nombre_usuario', sa.String(length=20), nullable=False),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=True),
    sa.Column('correo', sa.String(length=50), nullable=False),
    sa.Column('telefono', sa.String(length=20), nullable=False),
    sa.Column('clave_hash', sa.String(length=250), nullable=False),
    sa.Column('salt', sa.String(length=16), nullable=False),
    sa.Column('foto_perfil', sa.String(length=50), nullable=True),
    sa.Column('administrador', sa.Boolean(), nullable=False),
    sa.Column('suscripcion', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo'),
    sa.UniqueConstraint('nombre_usuario')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario')
    op.drop_table('producto')
    # ### end Alembic commands ###