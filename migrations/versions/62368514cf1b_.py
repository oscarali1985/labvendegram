"""empty message

Revision ID: 62368514cf1b
Revises: 
Create Date: 2020-10-14 11:24:00.731408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62368514cf1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    sa.Column('fecha_registro', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo'),
    sa.UniqueConstraint('nombre_usuario')
    )
    op.create_table('suscripcion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plan', sa.Enum('BASICO', name='planes'), nullable=False),
    sa.Column('fecha_registro', sa.Date(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tienda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_tienda', sa.String(length=40), nullable=False),
    sa.Column('correo_tienda', sa.String(length=30), nullable=False),
    sa.Column('telefono_tienda', sa.String(length=30), nullable=True),
    sa.Column('foto_tienda', sa.String(length=200), nullable=True),
    sa.Column('facebook_tienda', sa.String(length=30), nullable=True),
    sa.Column('instagram_tienda', sa.String(length=30), nullable=True),
    sa.Column('twitter_tienda', sa.String(length=30), nullable=True),
    sa.Column('zona_general', sa.Enum('DISTRITO_CAPITAL', 'MIRANDA', name='zona_general'), nullable=False),
    sa.Column('zona_uno', sa.Enum('ALTAGRACIA', 'ANTÍMANO', 'CANDELARIA', 'CARICUAO', 'CATEDRAL', 'CATIA', 'CAUCAGÜITA', 'CHACAO', 'COCHE', 'EL_CAFETAL', 'EL_JUNQUITO', 'EL_PARAÍSO', 'EL_RECREO', 'EL_VALLE', 'FILA_DE_MARICHES', 'LA_DOLORITA', 'LA_PASTORA', 'LA_VEGA', 'LAS_MINAS', 'LEONCIO_MARTÍNEZ', 'MACARAO', 'NUESTRA_SEÑORA_DEL_ROSARIO', 'PETARE', 'SAN_AGUSTÍN', 'SAN_BERNARDINO', 'SAN_JOSÉ', 'SAN_JUAN', 'SAN_PEDRO', 'SANTA_ROSALÍA', 'SANTA_ROSALÍA_DE_PALERMO', 'SANTA_TERESA', 'VEINTITRÉS_DE_ENERO', name='zona'), nullable=True),
    sa.Column('zona_dos', sa.Enum('ALTAGRACIA', 'ANTÍMANO', 'CANDELARIA', 'CARICUAO', 'CATEDRAL', 'CATIA', 'CAUCAGÜITA', 'CHACAO', 'COCHE', 'EL_CAFETAL', 'EL_JUNQUITO', 'EL_PARAÍSO', 'EL_RECREO', 'EL_VALLE', 'FILA_DE_MARICHES', 'LA_DOLORITA', 'LA_PASTORA', 'LA_VEGA', 'LAS_MINAS', 'LEONCIO_MARTÍNEZ', 'MACARAO', 'NUESTRA_SEÑORA_DEL_ROSARIO', 'PETARE', 'SAN_AGUSTÍN', 'SAN_BERNARDINO', 'SAN_JOSÉ', 'SAN_JUAN', 'SAN_PEDRO', 'SANTA_ROSALÍA', 'SANTA_ROSALÍA_DE_PALERMO', 'SANTA_TERESA', 'VEINTITRÉS_DE_ENERO', name='zona'), nullable=True),
    sa.Column('zona_tres', sa.Enum('ALTAGRACIA', 'ANTÍMANO', 'CANDELARIA', 'CARICUAO', 'CATEDRAL', 'CATIA', 'CAUCAGÜITA', 'CHACAO', 'COCHE', 'EL_CAFETAL', 'EL_JUNQUITO', 'EL_PARAÍSO', 'EL_RECREO', 'EL_VALLE', 'FILA_DE_MARICHES', 'LA_DOLORITA', 'LA_PASTORA', 'LA_VEGA', 'LAS_MINAS', 'LEONCIO_MARTÍNEZ', 'MACARAO', 'NUESTRA_SEÑORA_DEL_ROSARIO', 'PETARE', 'SAN_AGUSTÍN', 'SAN_BERNARDINO', 'SAN_JOSÉ', 'SAN_JUAN', 'SAN_PEDRO', 'SANTA_ROSALÍA', 'SANTA_ROSALÍA_DE_PALERMO', 'SANTA_TERESA', 'VEINTITRÉS_DE_ENERO', name='zona'), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo_tienda'),
    sa.UniqueConstraint('nombre_tienda')
    )
    op.create_table('producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=100), nullable=False),
    sa.Column('foto', sa.String(length=200), nullable=False),
    sa.Column('descripcion', sa.String(length=2000), nullable=False),
    sa.Column('precio', sa.Float(precision=10), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.Column('etiqueta_general', sa.Enum('PRODUCTOS', 'SERVICIOS', name='etiqueta_general'), nullable=False),
    sa.Column('etiqueta_uno', sa.Enum('ALIMENTOS', 'BEBIDAS', 'CEREALES', 'DECORACIONES', 'DETERGENTES', 'ENLATADOS', 'JABONES', 'MANTENIMIENTOS', 'MAQUILLAJES', 'MEDICAMENTOS', 'PELUQUERIA', 'PELUQUERIA_VETERINARIA', 'PLOMERIA', 'REPARACIONES', 'ROPA', 'SALSAS', name='etiqueta'), nullable=False),
    sa.Column('etiqueta_dos', sa.Enum('ALIMENTOS', 'BEBIDAS', 'CEREALES', 'DECORACIONES', 'DETERGENTES', 'ENLATADOS', 'JABONES', 'MANTENIMIENTOS', 'MAQUILLAJES', 'MEDICAMENTOS', 'PELUQUERIA', 'PELUQUERIA_VETERINARIA', 'PLOMERIA', 'REPARACIONES', 'ROPA', 'SALSAS', name='etiqueta'), nullable=True),
    sa.Column('etiqueta_tres', sa.Enum('ALIMENTOS', 'BEBIDAS', 'CEREALES', 'DECORACIONES', 'DETERGENTES', 'ENLATADOS', 'JABONES', 'MANTENIMIENTOS', 'MAQUILLAJES', 'MEDICAMENTOS', 'PELUQUERIA', 'PELUQUERIA_VETERINARIA', 'PLOMERIA', 'REPARACIONES', 'ROPA', 'SALSAS', name='etiqueta'), nullable=True),
    sa.Column('tienda_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tienda_id'], ['tienda.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('titulo')
    )
    op.create_table('producto_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('image_url', sa.String(length=500), nullable=False),
    sa.Column('public_id', sa.String(length=500), nullable=False),
    sa.Column('producto_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['producto_id'], ['producto.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('image_url'),
    sa.UniqueConstraint('public_id'),
    sa.UniqueConstraint('title', 'producto_id', name='unique_img_title_producto')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('producto_image')
    op.drop_table('producto')
    op.drop_table('tienda')
    op.drop_table('suscripcion')
    op.drop_table('usuario')
    # ### end Alembic commands ###