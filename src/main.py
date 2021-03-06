"""
Este modulo carga la Base de datos y agrega los endpoints
"""
import os
import uuid
from flask import Flask, request, jsonify, url_for, make_response, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, validate_email_syntax
from admin import setup_admin
from models import db, Usuario, Producto, Tienda, Suscripcion, ProductoImage
from smail import sendEmail
from stele import sendTelegram
from base64 import b64encode
import cloudinary.uploader as uploader
from werkzeug.utils import secure_filename
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
app = Flask(__name__, static_folder="static")
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024


app.config.from_mapping(
    CLOUDINARY_URL=os.environ.get("CLOUDINARY_URL")
)
# cloud_config.update = ({
#     "cloud_name": os.environ.get("CLOUD_NAME"),
#     "api_key": os.environ.get("API_KEY"),
#     "api_secret": os.environ.get("API_SECRET")
# })

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
MIGRATE = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
CORS(app)
setup_admin(app)


# Maneja/sereliza errores como un objeto JSON 26
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
# Genera el sitio con todos los endpoints cargados
@app.route('/')
def sitemap():
    return generate_sitemap(app)







########################45
#
#    Usuarios
#
########################
#Obtiene todos los nombres y filtra por nombre
@app.route("/usuario", methods=["GET", "POST"])
def cr_usuario():
    """
        "GET": devolver lista de todos los usuarios
        "POST": crear un usuario y devolver su información
    """

    # averiguar si es GET o POST
    if request.method == "GET":
        #   seleccionar todos los registros de la tabla usuarios usuarios - usando flask-sqlalchemy
        #   crear una variable lista y asignarle todos los usuarios que devuelva la consulta
        usuarios = Usuario.query.all()
        # verificamos si hay parámetros en la url y filtramos la lista con eso
        nombre = request.args.get("nombre")
        if nombre is not None:
            usuarios_filtrados = filter(lambda usuario: nombre.lower() in usuario.nombre_completo.lower(), usuarios)
        else:
            usuarios_filtrados = usuarios
        #   serializar los objetos de la lista - tendría una lista de diccionarios
        usuarios_serializados = list(map(lambda usuario: usuario.serializar(), usuarios_filtrados))
        #print(usuarios_serializados)
        #   devolver la lista jsonificada y 200_OK
        return jsonify(usuarios_serializados), 200
        
    else:
        #   crear una variable y asignarle diccionario con datos para crear usuario
        dato_reg = request.json # request.get_json()
        if dato_reg is None:
            return jsonify({
                "resultado": "no envió la informacion para crear el usuario..."
            }), 400
        #   verificar que el diccionario tenga los campos requeridos nombre, apellido, correo, telefono y clave
        if (
            "nombre" not in dato_reg or
            "apellido" not in  dato_reg or
            "nombre_usuario" not in dato_reg or
            "fecha_nacimiento"not in dato_reg or
            "correo" not in dato_reg or
            "telefono" not in dato_reg or
            "clave" not in dato_reg
        ):
            return jsonify({
                "resultado": "Favor verifique la informacion enviada faltan algunos campos obligatorios"
            }), 400
        #   validar que campos no vengan vacíos y que los campos cumplan con el modelo
        if (
            dato_reg["nombre"] == "" or
            dato_reg["apellido"] == "" or
            dato_reg["nombre_usuario"] == "" or
            dato_reg["correo"] == "" or
            len(str(dato_reg["nombre"])) >= 20 or
            len(str(dato_reg["apellido"])) >= 20 or
            len(str(dato_reg["nombre_usuario"])) >= 20 or
            len(str(dato_reg["correo"])) >= 50 or
            len(str(dato_reg["telefono"])) >= 20 or
            len(str(dato_reg["clave"])) >= 20 or
            len(str(dato_reg["foto_perfil"])) >= 50
        ):
            return jsonify({
                "resultado": "revise los valores de su solicitud"
            }), 400

        # Se procede a validar el correo
        validcorreo = validate_email_syntax(dato_reg["correo"])
        #print("Validando correo")
        #print(validcorreo)
        if validcorreo == True:

            #   crear una variable y asignarle el nuevo usuario con los datos validados
            nuevo_usuario = Usuario.registrarse(
                dato_reg["nombre"].lower().capitalize(),
                dato_reg["apellido"].lower().capitalize(),
                dato_reg["nombre_usuario"],
                dato_reg["fecha_nacimiento"],
                dato_reg["correo"].casefold(),
                dato_reg["telefono"],
                dato_reg["clave"],
                dato_reg["foto_perfil"],
                dato_reg["administrador"],
                dato_reg["suscripcion"]
            )
            
            #   agregar a la sesión de base de datos (sqlalchemy) y hacer commit de la transacción
            db.session.add(nuevo_usuario)
            try:
                db.session.commit()
                #titulocorreo= "Registro satisfactorio"
                #nombre=dato_reg["nombre"]
                #correo=dato_reg["correo"]
                #nombreusuario=dato_reg["nombre_usuario"]
                #mensaje = f"gracias por registrarse su usuario es {nombreusuario}"
                #email = sendEmail(titulocorreo, nombre, correo, mensaje)
                # devolvemos el nuevo usuario serializado y 201_CREATED
                return jsonify(nuevo_usuario.serializar()), 201
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                # devolvemos "mira, tuvimos este error..."
                return jsonify({
                    "resultado": f"{error.args}"
                }), 500
        else:
            #Correo invalido
            status_code = 400
            response_body = {
                "result": "HTTP_400_BAD_REQUEST. Verifique el correo ingresado."
            }
            return  jsonify(response_body), status_code

#Obtiene usuarios segun su id para acualizar o eliminar solo por admin
@app.route("/usuario/<id>", methods=["GET", "PUT", "DELETE"])
@jwt_required

def crud_usuario(id):
    """
        GET: devolver el detalle de un usuario específico
        PUT actualizar datos del usuario específico,
            guardar en base de datos y devolver el detalle
        DELETE: eliminar el usuario específico y devolver 204 
    """
    usuario_id_jwt = get_jwt_identity()
    usuario= Usuario.query.get(usuario_id_jwt)
    admin = usuario.administrador
    #print(usuario_id_jwt)
    #print(usuario)
    #print(admin)

    if (admin == True):
        #
        # crear una variable y asignar el usuario específico
            usuario = Usuario.query.get(id)
            # verificar si el usuario con id usuario_id existe
            if isinstance(usuario, Usuario):
                if request.method == "PUT":
                    # recuperar diccionario con insumos del body del request
                    diccionario = request.get_json()
                    # actualizar propiedades que vengan en el diccionario
                    #print(diccionario)
                    usuario.actualizar_usuario(diccionario)
                    # guardar en base de datos, hacer commit
                    try:
                        db.session.commit()
                        # devolver el usuario serializado y jsonificado. Y 200 
                        return jsonify(usuario.serializar()), 200
                    except Exception as error:
                        db.session.rollback()
                        print(f"{error.args} {type(error)}")
                        return jsonify({
                            "resultado": f"{error.args}"
                        }), 500
                else:
                    # remover el usuario específico de la sesión de base de datos
                    db.session.delete(usuario)
                    # hacer commit y devolver 204
                    try:
                        db.session.commit()
                        return jsonify({
                            "resultado": "el contacto fue eliminado"
                        }), 204
                    except Exception as error:
                        db.session.rollback()
                        print(f"{error.args} {type(error)}")
                        return jsonify({
                            "resultado": f"{error.args}"
                        }), 500
            else:
                # el usuario no existe!
                return jsonify({
                    "resultado": "el contacto que ingreso no existe..."
                }), 404

    else:
        # el usuario no existe!
        return jsonify({
                    "resultado": "No tiene permiso para realizar esta operacion"
                }), 404

    

@app.route('/usuario/<int:usuario_id>', methods=["GET"])
def getSpecificUsuario(usuario_id):

    if request.method == "GET":
        usuario = Usuario.query.filter(Usuario.id == usuario_id)
        usuario_list = list(map(lambda usuario: usuario.serializar(), usuario))

        if usuario_list == []:
            msj="no se encontro el usuario ingresado"
            return jsonify(msj), 200
        else:
            return jsonify(usuario_list), 200
    else:
            response_body = {"msj":"Metodo invalido request"}
            return jsonify(response_body), 400
















########################159
#
#    Suscripcion
#
########################



@app.route('/suscripcion', methods=["GET", "POST"])

def todos_Suscripcion():
    if request.method == "GET":
        suscripcion = Suscripcion.query.all()
        # verificamos si hay parámetros en la url y filtramos la lista con eso si titulo no esta vacio producto_filtrado busca en producto.titulo si el requerimiento es igual a algun titulo ya creado para filtrarlo.
        plan = request.args.get("plan")
        if plan is not None:
            suscripcion_filtrado = filter(lambda suscripcion: plan.lower() in suscripcion.plan, suscripcion) 
        else:
            suscripcion_filtrado = suscripcion
        #   serializar los objetos de la lista - tendría una lista de diccionarios
        suscripcion_lista = list(map(lambda suscripcion: suscripcion.serialize(), suscripcion_filtrado))     
        return jsonify(suscripcion_lista), 200
   ###Validaciones de caracteres y que los campos no esten vacios###
    else:
        insumos_producto = request.json
        if insumos_producto is None:
            return jsonify({
                "resultado": "no envio insumos para crear el producto" 
            }), 400

        # METODO POST: crear una variable y asignarle el nuevo producto con los datos validados

        body = request.get_json()        
        suscripcion = Suscripcion(plan=body['plan'])
        #   agregar a la sesión de base de datos (sqlalchemy) y hacer commit de la transacción
        db.session.add(suscripcion)
        try:
            db.session.commit()
            # devolvemos el nuevo donante serializado y 201_CREATED
            return jsonify(suscripcion.serialize()), 201
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            # devolvemos "mira, tuvimos este error..."
            return jsonify({
                "resultado2": f"{error.args}"
            }), 500

##########  4.- Eliminar un producto DELETE /producto/{producto_id} ########### 

@app.route('/suscripcion/<int:suscripcion_id>', methods=['DELETE'])
def eliminar_suscripcion(suscripcion_id):
    suscripcion = Suscripcion.query.get(suscripcion_id)
    if suscripcion is None:
        raise APIException('suscripcion no encontrado', status_code=404)
    else:
        # remover el suscripcion específico de la sesión de base de datos
        db.session.delete(suscripcion)
        # hacer commit y devolver 200
        try:
            db.session.commit()
            response_body = {
           "msg": "La suscripcion a sido eliminada"
           }
            return jsonify(response_body), 200
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "resultado al eliminar una suscripcion": f"{error.args}"
            }), 500


##########  5.- Actualiza el suscripcion UPDATE /producto/{producto_id} ###########     
@app.route('/suscripcion/<int:suscripcion_id>', methods=['PUT'])
def actualizar_suscripcion(suscripcion_id):
    body = request.get_json()
    suscripcion = Suscripcion.query.get(suscripcion_id)
    if suscripcion is None:
        raise APIException('suscripcion no encontrado', status_code=404) 
    suscripcion.update(body)
    try:
        db.session.commit()
        # devolvemos el nuevo suscripcion serializado y 200_CREATED
        return jsonify(suscripcion.serialize()), 200
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        # devolvemos "mira, tuvimos este error..."
        return jsonify({
            "Presente error al actualizar un suscripcion": f"{error.args}"
        }), 500    


@app.route('/suscripcion/<int:suscripcion_id>', methods=["GET"])
def getSpecificSuscripcion(suscripcion_id):

    if request.method == "GET":
        suscripcion = Suscripcion.query.filter(Suscripcion.id == suscripcion_id)
        suscripcion_list = list(map(lambda suscripcion: suscripcion.serialize(), suscripcion))

        if suscripcion_list == []:
            msj="no se encontro la suscripcion ingresada"
            return jsonify(msj), 200
        else:
            return jsonify(suscripcion_list), 200
    else:
            response_body = {"msj":"Metodo invalido request"}
            return jsonify(response_body), 400






























########################201
#
#    Tienda
#
########################

###################        CRUD de Vendegram !!!    ######################  
#####  1.-Obtenga una lista de todos las tiendas GET /tienda;                         tambien filtra por nombre si recibe el parametro en la url   #########
    ##########  2.- Crear un nuevo tienda POST / ########### 

@app.route('/tienda', methods=["GET"])

def todos_tiendas():
    if request.method == "GET":
        tienda = Tienda.query.all()
        # verificamos si hay parámetros en la url y filtramos la lista con eso si titulo no esta vacio producto_filtrado busca en producto.titulo si el requerimiento es igual a algun titulo ya creado para filtrarlo.
        nombre_tienda = request.args.get("nombre_tienda")
        if nombre_tienda is not None:
            tienda_filtrado = filter(lambda tienda: nombre_tienda.lower() in tienda.nombre_tienda, tienda) 
        else:
            tienda_filtrado = tienda
        #   serializar los objetos de la lista - tendría una lista de diccionarios
        tienda_lista = list(map(lambda tienda: tienda.serialize(), tienda_filtrado))     
        return jsonify(tienda_lista), 200
   ###Validaciones de caracteres y que los campos no esten vacios###
    else:
        insumos_tienda = request.json
        if insumos_tienda is None:
            return jsonify({
                "resultado": "no envio insumos para crear la tienda" 
            }), 400
         # verificar que el diccionario tenga titulo, descripcion, foto,etc
        if (
            "nombre_tienda" not in insumos_tienda or
            "correo_tienda" not in insumos_tienda or
            "telefono_tienda" not in insumos_tienda or
            "foto_tienda" not in insumos_tienda or
            "zona_general" not in insumos_tienda or
            "zona_uno" not in insumos_tienda or
            "zona_dos" not in insumos_tienda
        ):
            return jsonify({
                "resultado": "revise las propiedades de su solicitud"
            }), 400
        #validar que campos no vengan vacíos y que los string tenga sus respectivos caracteres
        if (
            insumos_tienda["nombre_tienda"] == "" or
            # insumos_producto["descripcion"] == "" or
            insumos_tienda["correo_tienda"] == "" or
            insumos_tienda["zona_general"] == "" or 
            # insumos_producto["etiqueta_uno"] == "" or         
            len(str(insumos_tienda["nombre_tienda"])) > 40 or
            # len(str(insumos_producto["descripcion"])) > 2000 or
            len(str(insumos_tienda["correo_tienda"])) > 30
            # int(insumos_producto["cantidad"]) < 0 or
            # float(insumos_producto["precio"]) < 0

        ):
            return jsonify({
                "resultado": "revise los valores de su solicitud"
            }), 400



@app.route('/tienda', methods=["POST"])

def post_tiendas():
        if request.method == "POST":
            
        # METODO POST: crear una variable y asignarle el nuevo tienda con los datos validados
            body = request.get_json()    

            #Se valida si la usuario existe
            usuario = Usuario.query.get(body['usuario_id'])
            if usuario is None:
                raise APIException(f'La usuario a la cual se desea agregar el tienda no existe, Verifique la infomracion', status_code=404)
            else:
                tienda = Tienda(nombre_tienda=body['nombre_tienda'], correo_tienda=body['correo_tienda'], telefono_tienda=body['telefono_tienda'],
                foto_tienda=body['foto_tienda'], facebook_tienda=body['facebook_tienda'], instagram_tienda=body['instagram_tienda'], 
                twitter_tienda=body['twitter_tienda'],zona_general=body['zona_general'],zona_uno=body['zona_uno'],zona_dos=body['zona_dos'],zona_tres=body['zona_tres'],usuario_id=body['usuario_id'] )
                #   agregar a la sesión de base de datos (sqlalchemy) y hacer commit de la transacción
                print("imprimiento")
                print (jsonify(tienda.serializer()))
                db.session.add(tienda)
            try:
                db.session.commit()
                # devolvemos el nuevo donante serializado y 201_CREATED
                return jsonify(tienda.serialize()), 201
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                # devolvemos "mira, tuvimos este error..."
                return jsonify({
                    "resultado1": f"{error.args}"
                }), 500



@app.route('/tienda/<int:tienda_id>', methods=['DELETE'])
def eliminar_tienda(tienda_id):
    tienda = Tienda.query.get(tienda_id)
    if tienda is None:
        raise APIException('tienda no encontrado', status_code=404)
    else:
        # remover el tienda específico de la sesión de base de datos
        db.session.delete(tienda)
        # hacer commit y devolver 200
        try:
            db.session.commit()
            response_body = {
           "msg": "La tienda a sido eliminado"
           }
            return jsonify(response_body), 200
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "resultado al eliminar una tienda": f"{error.args}"
            }), 500


##########  5.- Actualiza el tienda UPDATE /producto/{producto_id} ###########     
@app.route('/tienda/<int:tienda_id>', methods=['PUT'])
def actualizar_tienda(tienda_id):
    body = request.get_json()
    tienda = Tienda.query.get(tienda_id)
    if tienda is None:
        raise APIException('tienda no encontrado', status_code=404) 
    tienda.update(body)
    try:
        db.session.commit()
        # devolvemos el nuevo tienda serializado y 200_CREATED
        return jsonify(tienda.serialize()), 200
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        # devolvemos "mira, tuvimos este error..."
        return jsonify({
            "Presente error al actualizar un tienda": f"{error.args}"
        }), 500    




@app.route('/tienda/<int:tienda_id>', methods=["GET"])
def getSpecificTienda(tienda_id):

    if request.method == "GET":
        tienda = Tienda.query.filter(Tienda.id == tienda_id)
        tienda_list = list(map(lambda tienda: tienda.serialize(), tienda))

        if tienda_list == []:
            msj="no se encontro la tienda ingresada"
            return jsonify(msj), 200
        else:
            return jsonify(tienda_list), 200
    else:
            response_body = {"msj":"Metodo invalido request"}
            return jsonify(response_body), 400








########################201
#
#    Productos
#
########################


###################        CRUD de Vendegram !!!    ######################  
#####  1.-Obtenga una lista de todos los productos GET /producto;                         tambien filtra por nombre si recibe el parametro en la url   #########
    ##########  2.- Crear un nuevo producto POST /producto ########### 

@app.route('/producto', methods=["GET"])

def todos_productos():
    if request.method == "GET":
        producto = Producto.query.all()
        # verificamos si hay parámetros en la url y filtramos la lista con eso si titulo no esta vacio producto_filtrado busca en producto.titulo si el requerimiento es igual a algun titulo ya creado para filtrarlo.
        titulo = request.args.get("titulo")
        etiqueta = request.args.get("etiqueta")
        zona = request.args.get("zona")
        match_all = request.args.get("all")

        if titulo is not None and etiqueta is None and zona is None:
            producto_filtrado = filter(lambda producto:(
            titulo.lower() in producto.titulo.lower()), producto)
        else:
            producto_filtrado = producto    

            if etiqueta is not None and titulo is None and zona is None:
                producto_filtrado = filter(lambda producto:(
                str(etiqueta) in str(producto.etiqueta_general).lower() or
                str(etiqueta) in str(producto.etiqueta_uno).lower() or
                str(etiqueta) in str(producto.etiqueta_dos).lower() or
                str(etiqueta) in str(producto.etiqueta_tres).lower()), producto)
            else:
                producto_filtrado = producto

                if zona is not None and titulo is None and etiqueta is None:
                    producto_filtrado = filter(lambda producto:(
                    str(zona) in str(producto.tienda.zona_general).lower() or
                    str(zona) in str(producto.tienda.zona_uno).lower() or
                    str(zona) in str(producto.tienda.zona_dos).lower() or
                    str(zona) in str(producto.tienda.zona_tres).lower()), producto)
                else:
                    producto_filtrado = producto 

                    if titulo and etiqueta is not None and zona is None:
                        producto_filtrado = filter(lambda producto:(
                        titulo.lower() in producto.titulo.lower() and 
                        str(etiqueta) in str(producto.etiqueta_general).lower() or
                        titulo.lower() in producto.titulo.lower() and 
                        str(etiqueta) in str(producto.etiqueta_uno).lower() or
                        titulo.lower() in producto.titulo.lower() and 
                        str(etiqueta) in str(producto.etiqueta_dos).lower() or
                        titulo.lower() in producto.titulo.lower() and 
                        str(etiqueta) in str(producto.etiqueta_tres).lower()), producto)
                    else:
                        producto_filtrado = producto
                        
                        if titulo and zona is not None and etiqueta is None:
                            producto_filtrado = filter(lambda producto:(
                            titulo.lower() in producto.titulo.lower() and
                            str(zona) in str(producto.tienda.zona_general).lower() or
                            titulo.lower() in producto.titulo.lower() and
                            str(zona) in str(producto.tienda.zona_uno).lower() or
                            titulo.lower() in producto.titulo.lower() and
                            str(zona) in str(producto.tienda.zona_dos).lower() or
                            titulo.lower() in producto.titulo.lower() and
                            str(zona) in str(producto.tienda.zona_tres).lower()), producto)
                        else:
                            producto_filtrado = producto

                            if etiqueta and zona is not None and titulo is None:
                                producto_filtrado = filter(lambda producto:(
                                str(etiqueta) in str(producto.etiqueta_general).lower() and
                                str(zona) in str(producto.tienda.zona_general).lower() or
                                str(etiqueta) in str(producto.etiqueta_general).lower() and
                                str(zona) in str(producto.tienda.zona_uno).lower() or 
                                str(etiqueta) in str(producto.etiqueta_general).lower() and
                                str(zona) in str(producto.tienda.zona_dos).lower() or 
                                str(etiqueta) in str(producto.etiqueta_general).lower() and
                                str(zona) in str(producto.tienda.zona_tres).lower() or

                                str(etiqueta) in str(producto.etiqueta_uno).lower() and
                                str(zona) in str(producto.tienda.zona_general).lower() or 
                                str(etiqueta) in str(producto.etiqueta_uno).lower() and
                                str(zona) in str(producto.tienda.zona_uno).lower() or 
                                str(etiqueta) in str(producto.etiqueta_uno).lower() and
                                str(zona) in str(producto.tienda.zona_dos).lower() or  
                                str(etiqueta) in str(producto.etiqueta_uno).lower() and
                                str(zona) in str(producto.tienda.zona_tres).lower() or 

                                str(etiqueta) in str(producto.etiqueta_dos).lower() and
                                str(zona) in str(producto.tienda.zona_general).lower() or 
                                str(etiqueta) in str(producto.etiqueta_dos).lower() and
                                str(zona) in str(producto.tienda.zona_uno).lower() or 
                                str(etiqueta) in str(producto.etiqueta_dos).lower() and
                                str(zona) in str(producto.tienda.zona_dos).lower() or  
                                str(etiqueta) in str(producto.etiqueta_dos).lower() and
                                str(zona) in str(producto.tienda.zona_tres).lower() or 

                                str(etiqueta) in str(producto.etiqueta_tres).lower() and
                                str(zona) in str(producto.tienda.zona_general).lower() or 
                                str(etiqueta) in str(producto.etiqueta_tres).lower() and
                                str(zona) in str(producto.tienda.zona_uno).lower() or 
                                str(etiqueta) in str(producto.etiqueta_tres).lower() and
                                str(zona) in str(producto.tienda.zona_dos).lower() or  
                                str(etiqueta) in str(producto.etiqueta_tres).lower() and
                                str(zona) in str(producto.tienda.zona_tres).lower() 
                                ), producto)
                            else:
                                producto_filtrado = producto

                                if titulo and etiqueta and zona is not None:
                                    if match_all == "True":
                                        producto_filtrado = filter(lambda producto: ( 
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_general).lower() and 
                                            str(zona) in str(producto.tienda.zona_general).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_general).lower() and 
                                            str(zona) in str(producto.tienda.zona_uno).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_general).lower() and 
                                            str(zona) in str(producto.tienda.zona_dos).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_general).lower() and 
                                            str(zona) in str(producto.tienda.zona_tres).lower() or 

                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_uno).lower() and 
                                            str(zona) in str(producto.tienda.zona_general).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_uno).lower() and 
                                            str(zona) in str(producto.tienda.zona_uno).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_uno).lower() and 
                                            str(zona) in str(producto.tienda.zona_dos).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_uno).lower() and 
                                            str(zona) in str(producto.tienda.zona_tres).lower() or
                                            
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_dos).lower() and 
                                            str(zona) in str(producto.tienda.zona_general).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_dos).lower() and 
                                            str(zona) in str(producto.tienda.zona_uno).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_dos).lower() and 
                                            str(zona) in str(producto.tienda.zona_dos).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_dos).lower() and 
                                            str(zona) in str(producto.tienda.zona_tres).lower() or

                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_tres).lower() and 
                                            str(zona) in str(producto.tienda.zona_general).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_tres).lower() and 
                                            str(zona) in str(producto.tienda.zona_uno).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_tres).lower() and 
                                            str(zona) in str(producto.tienda.zona_dos).lower() or
                                            titulo.lower() in producto.titulo.lower() and 
                                            str(etiqueta) in str(producto.etiqueta_tres).lower() and 
                                            str(zona) in str(producto.tienda.zona_tres).lower() 
                                            ), producto)              
                                    else:
                                        producto_filtrado = filter(lambda producto: ( 
                                            titulo.lower() in producto.titulo.lower() or 
                                            str(etiqueta) in str(producto.etiqueta_general).lower() or 
                                            str(zona) in str(producto.tienda.zona_general).lower()
                                            ), producto)
                                else:
                                    producto_filtrado = producto
        producto_lista = list(map(lambda producto: producto.serialize(), producto_filtrado))
        return jsonify(producto_lista), 200
    else:
        insumos_producto = request.json
        if insumos_producto is None:
            return jsonify({
                "resultado": "no envio insumos para crear el producto" 
            }), 400
         # verificar que el diccionario tenga titulo, descripcion, foto,etc
        if (
            "titulo" not in insumos_producto or
            "descripcion" not in insumos_producto or
            "foto" not in insumos_producto or
            "cantidad" not in insumos_producto or
            "precio" not in insumos_producto or
            "etiqueta_general" not in insumos_producto or
            "etiqueta_uno" not in insumos_producto
        ):
            return jsonify({
                "resultado": "revise las propiedades de su solicitud"
            }), 400
        #validar que campos no vengan vacíos y que los string tenga sus respectivos caracteres
        if (
            insumos_producto["titulo"] == "" or
            insumos_producto["descripcion"] == "" or
            insumos_producto["foto"] == "" or
            insumos_producto["etiqueta_general"] == "" or 
            insumos_producto["etiqueta_uno"] == "" or         
            len(str(insumos_producto["titulo"])) > 100 or
            len(str(insumos_producto["descripcion"])) > 2000 or
            len(str(insumos_producto["foto"])) > 200 or
            int(insumos_producto["cantidad"]) < 0 or
            float(insumos_producto["precio"]) < 0

        ):
            return jsonify({
                "resultado": "revise los valores de su solicitud"
            }), 400


@app.route('/producto', methods=["POST"])

def post_productos():
        if request.method == "POST":
            
        # METODO POST: crear una variable y asignarle el nuevo producto con los datos validados
            body = request.get_json()    

            #Se valida si la tienda existe
            tienda = Tienda.query.get(body['tienda_id'])
            if tienda is None:
                raise APIException(f'La tienda a la cual se desea agregar el producto no existe, Verifique la infomracion', status_code=404)
            else:
                producto = Producto(titulo=body['titulo'], foto=body['foto'], descripcion=body['descripcion'],
                precio=body['precio'], cantidad=body['cantidad'], etiqueta_uno=body['etiqueta_uno'], 
                etiqueta_dos=body['etiqueta_dos'],etiqueta_tres=body['etiqueta_tres'],etiqueta_general=body['etiqueta_general'], tienda_id=body['tienda_id'] )
                #   agregar a la sesión de base de datos (sqlalchemy) y hacer commit de la transacción
                print("imprimiento")
                print (jsonify(producto.serializer()))
                db.session.add(producto)
            try:
                db.session.commit()
                # devolvemos el nuevo donante serializado y 201_CREATED
                return jsonify(producto.serialize()), 201
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                # devolvemos "mira, tuvimos este error..."
                return jsonify({
                    "resultado1": f"{error.args}"
                }), 500

##########  4.- Eliminar un producto DELETE /producto/{producto_id} ########### 

@app.route('/producto/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if producto is None:
        raise APIException('producto no encontrado', status_code=404)
    else:
        # remover el producto específico de la sesión de base de datos
        db.session.delete(producto)
        # hacer commit y devolver 200
        try:
            db.session.commit()
            response_body = {
           "msg": "El producto a sido eliminado"
           }
            return jsonify(response_body), 200
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "resultado al eliminar un producto": f"{error.args}"
            }), 500


##########  5.- Actualiza el producto UPDATE /producto/{producto_id} ###########     
@app.route('/producto/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    body = request.get_json()
    producto = Producto.query.get(producto_id)
    if producto is None:
        raise APIException('producto no encontrado', status_code=404) 
    producto.update(body)
    try:
        db.session.commit()
        # devolvemos el nuevo producto serializado y 200_CREATED
        return jsonify(producto.serialize()), 200
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        # devolvemos "mira, tuvimos este error..."
        return jsonify({
            "Presente error al actualizar un producto": f"{error.args}"
        }), 500    


@app.route('/producto/<int:producto_id>', methods=["GET"])
def getSpecificproducto(producto_id):

    if request.method == "GET":
        #producto = Producto.query.filter(Producto.id == producto_id)
        producto = Producto.query.filter_by(id=producto_id).one_or_none()
        print
        #producto_list = list(map(lambda producto: producto.serialize(), producto))
        producto_list = {}
        #print(producto_list)
        #print(type(producto_list))

        if not producto  :
            msj="no se encontro el producto ingresado"
            return jsonify(msj), 400
        else:
            producto_list = producto.serialize()
            return jsonify(producto_list), 200
    else:
            response_body = {"msj":"Metodo invalido request"}
            return jsonify(response_body), 400

@app.route('/productot/<int:tienda_id>', methods=["GET"])
def getProductosbytienda(tienda_id):

    if request.method == "GET":
        #producto = Producto.query.filter(Producto.id == producto_id)
        producto = Producto.query.filter_by(tienda_id=tienda_id)
        
        producto_list = list(map(lambda producto: producto.serialize(), producto))
        
        #print(producto_list)
        #print(type(producto_list))

        if not producto_list  :
            msj="no se encontro el producto ingresado"
            return jsonify(msj), 400
        else:
            
            return jsonify(producto_list), 200
    else:
            response_body = {"msj":"Metodo invalido request"}
            return jsonify(response_body), 400

















########################917
#
#    Enviar ccorreo o mensajes telegram
#
########################

#Para enviar correo usando la cuenta de VendeGram
@app.route("/SendCorreo", methods = ['POST'])
def SendCorreo():

    # Verificamos el método
    if (request.method == 'POST'):

        # Obtenemos los datos de la forma
        titulocorreo = request.form['titulocorreo']
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']
        respuesta = sendEmail(titulocorreo, nombre, correo, mensaje)
        #flash(respuesta, 'alert-success')
        #print(respuesta)
        # Redirigimos a mensaje
        return jsonify(respuesta), 200

# Para enviar mensajes por Telegram mendiante su API
@app.route("/SendTelegram", methods = ['POST'])
def SendTelegram():

    # Verificamos el método
    if (request.method == 'POST'):

        # Obtenemos los datos de la forma
        
        nombre = request.form['nombre']
        telegram = request.form['telegram']
        mensaje = request.form['mensaje']

        #idTelegram = " {} "+telegram
        response = sendTelegram(nombre, telegram, mensaje)
        
        return response


########################960
#
#    Login
#
########################

@app.route("/ingresar", methods = ['POST'])
def manejar_ingreso():
    '''
    POST: Se verifica si el usuario existe y luego se verifica la clave. Se recibe el correo y clave
    '''

    input_data = request.json
    if ("correo" not in input_data or
        "clave" not in input_data 
    ):
        return jsonify({
            "resultado":"favor ingresar la el usuario o clave para verificar la informacion"
            }),400

    else:
        usuario = Usuario.query.filter_by(
            correo=input_data["correo"]
        ).one_or_none()
        if usuario is None:
            return jsonify({
            "resultado":"La informacion ingresada es incorrecta valide sus datos"
            }), 400
        else:
            if usuario.check_password(input_data["clave"]):
                #exito
                jwt = create_jwt(identity = usuario.id)
                reenvio = usuario.serializar()
                reenvio["jwt"] = jwt
                return jsonify(reenvio), 200
            else:
                return jsonify({
            "resultado":"Verifique su clave"
            }), 400


#Obtiene usuarios segun su id para acualizar o eliminar solo por admin
@app.route("/cambiouclauario/<id>", methods=["PUT"])
@jwt_required

def cambiocusuario(id):
    """
        PUT Se actualiza la clave del usuario. Se debe enviar la clave
    """
    usuario_id_jwt = get_jwt_identity()
    usuario= Usuario.query.get(usuario_id_jwt)
    admin = usuario.administrador
    #print(usuario_id_jwt)
    #print(usuario)
    #print(admin)

    if (admin == True):
        #
        # crear una variable y asignar el usuario específico
            usuario = Usuario.query.get(id)
            # verificar si el usuario con id usuario_id existe
            if isinstance(usuario, Usuario):
                if request.method == "PUT":
                    # recuperar diccionario con insumos del body del request
                    diccionario = request.get_json()
                    # actualizar propiedades que vengan en el diccionario
                    #print(diccionario)
                    usuario.actualizar_clave(diccionario)
                    # guardar en base de datos, hacer commit
                    try:
                        db.session.commit()
                        # devolver el usuario serializado y jsonificado. Y 200 
                        return jsonify({
                                        "resultado": f"La clave del usuario {usuario.id} ha sido actualizada"
                                    }), 200
                    except Exception as error:
                        db.session.rollback()
                        print(f"{error.args} {type(error)}")
                        return jsonify({
                            "resultado": f"{error.args}"
                        }), 500

            else:
                # el usuario no existe!
                return jsonify({
                    "resultado": "el contacto que ingreso no existe..."
                }), 404

    else:
        # el usuario no existe!
        return jsonify({
                    "resultado": "No tiene permiso para realizar esta operacion"
                }), 404

@app.route("/cambioclaveale/<id>", methods=["PUT",])
@jwt_required

def cambioclavealetaria(id):
    """
        PUT actualizar la clave de un usuario en particular
    """
    usuario_id_jwt = get_jwt_identity()
    usuario= Usuario.query.get(usuario_id_jwt)
    admin = usuario.administrador
    #print(usuario_id_jwt)
    #print(usuario)
    #print(admin)

    if (admin == True):
        #
        # crear una variable y asignar el usuario específico
            usuario = Usuario.query.get(id)
            # verificar si el usuario con id usuario_id existe
            if isinstance(usuario, Usuario):
                if request.method == "PUT":
                    # recuperar diccionario con insumos del body del request
                    nuevaclave = b64encode(os.urandom(4)).decode("utf-8")
                    # actualizar propiedades que vengan en el diccionario
                    usuario.actualizar_clavealeatoria(nuevaclave)
                    # guardar en base de datos, hacer commit
                    try:
                        db.session.commit()
                        titulocorreo= "Cambio de clave satisfactorio"
                        nombre=usuario.nombre
                        correo=usuario.correo
                        mensaje = f"Se ha realizado un cambio de clave '{nuevaclave}' "
                        email = sendEmail(titulocorreo, nombre, correo, mensaje)
                        # devolver el usuario serializado y jsonificado. Y 200 
                        return jsonify({
                                        "resultado": f"La clave del usuario {usuario.id} ha sido actualizada y enviada por correo"
                                    }), 200
                    except Exception as error:
                        db.session.rollback()
                        print(f"{error.args} {type(error)}")
                        return jsonify({
                            "resultado": f"{error.args}"
                        }), 500

            else:
                # el usuario no existe!
                return jsonify({
                    "resultado": "el contacto que ingreso no existe..."
                }), 404

    else:
        # el usuario no existe!
        return jsonify({
                    "resultado": "No tiene permiso para realizar esta operacion"
                }), 404

@app.route("/cambioclavecorreo/<nombre_usuario>", methods=["PUT"])

def cambioclavecorreo(nombre_usuario):
    """
        PUT actualizar la clave de un usuario en particular
    """
    usuariob = nombre_usuario
    correovalid=False
    usuariovalid= False
    #print(usuariob)
    # crear una variable y asignar el usuario específico
    usuario=Usuario.query.filter(Usuario.nombre_usuario.like(usuariob))
    correo=Usuario.query.filter(Usuario.correo.like(usuariob))
    #usuario = Usuario.query.filter(OR (Usuario.nombre_usuario.like(usuariob), Usuario.correo.like(usuariob)))
    #usuario = Usuario.query.filter(Usuario.nombre_usuario == "oscaralidiaz")
    #usuario = Usuario.query.get(nombre_usuario)
    for row in usuario:
        if (row.nombre_usuario==usuariob):
            usuariovalid= True
            usuario = Usuario.query.get(row.id)
        #print ("ID:", row.id, "Name: ",row.nombre_usuario, "Email:",row.correo)
    for row in correo:
        if (row.correo==usuariob):
            correovalid= True
            usuario = Usuario.query.get(row.id)
        #print ("ID:", row.id, "Name: ",row.nombre_usuario, "Email:",row.correo)    
    
    #print(usuario)
    
    
    # verificar si el usuario con id usuario_id existe
    if (correovalid== True or usuariovalid== True):
        #print(usuario)
        if request.method == "PUT":
            # recuperar diccionario con insumos del body del request
            nuevaclave = b64encode(os.urandom(4)).decode("utf-8")
            # actualizar propiedades que vengan en el diccionario
            usuario.actualizar_clavealeatoria(nuevaclave)
            # guardar en base de datos, hacer commit
            try:
                db.session.commit()
                titulocorreo= "Cambio de clave satisfactorio"
                nombre=usuario.nombre
                correo=usuario.correo
                mensaje = f"Se ha realizado un cambio de clave '{nuevaclave}' "
                email = sendEmail(titulocorreo, nombre, correo, mensaje)
                # devolver el usuario serializado y jsonificado. Y 200 
                return jsonify({
                                "resultado": f"La clave del usuario {usuario.id} ha sido actualizada y enviada por correo"
                                }), 200
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                        "resultado": f"{error.args}"
                    }), 500

    else:
        # el usuario no existe!
        return jsonify({
                    "resultado": "el contacto que ingreso no existe..."
                }), 404




















########################1192
#
#    Claudinary
#
########################




# producto images endpoint
@app.route("/producto/<int:producto_id>/images", methods=["POST", "GET"])
@app.route("/producto/<int:producto_id>/images/<int:id>", methods=["DELETE"])
def handle_producto_images(producto_id, id=None):
    """ 
        GET to receive all producto images as a list of objects,
        POST to create a new producto image.
    """
    headers = {
        "Content-Type": "application/json"
    }
    # check if producto exists
    if Producto.query.filter_by(id=producto_id).first():
        # producto exists

        if request.method == "GET":
            # get producto images and return them
            # producto_images = ProductoImage.query.filter(Producto.id == producto_id).all()
            producto_images = ProductoImage.query.filter_by(producto_id=producto_id).all()
            response_body = []
            
            if len(producto_images) > 0:
                for image in producto_images:
                    response_body.append(image.serialize())
                status_code = 200
            else:
                response_body = []
                status_code = 200

        elif request.method == "POST":
            # produc = Producto.query.all()
            # titu = request.args.get(id)
            # check if producto has less than 5 images stored
            # if len(ProductoImage.query.filter(Producto.id == producto_id).all()) < 5:
            # if len(UserImage.query.filter_by(user_username=username).all()) < 5:
            if len(ProductoImage.query.filter_by(producto_id=producto_id).all()) < 3:
                # receive file, secure its name, save it and
                # create object to store title and image_url

                # podria ser el error aqui en el target?


                target = os.path.join(UPLOAD_FOLDER, "images")
                if not os.path.isdir(target):
                    os.mkdir(target)  
                try:
                    image_file = request.files['file']
                    filename = secure_filename(image_file.filename)
                    extension = filename.rsplit(".", 1)[1]
                    hash_name = uuid.uuid4().hex
                    hashed_filename = ".".join([hash_name, extension])
                    destination = os.path.join(target, hashed_filename)
                    response = uploader.upload(image_file)
                    print(f"{response.items()}")                      
                    # sorry es este try, exacto q no teniamos file :s
                    # alli estaba username, pero era para el endpoint /ernesto/image
                    #entonces yo lo cambie a producto/<int:producto_id>/images
                    # dice que title no esta definido en la linea 1244
                    
                    try:
                        new_image = ProductoImage(request.form.get("title"), response["public_id"], response["secure_url"], producto_id)                        
                        # new_image = ProductoImage(request.form.get("title"), destination, producto_id)
                        db.session.add(new_image)  
                       

                        try:
                            db.session.commit()
                            # image_file.save(destination)
                            response_body = {
                                "result": "HTTP_201_CREATED. image created for producto"
                            }
                            status_code = 201
                        # except IntegrityError:
                        except Exception as error:
                            db.session.rollback()
                            response_body = {
                                "result": f"HTTP_400_BAD_REQUEST. {type(error)} {error.args}"
                            }
                            status_code = 400
                    except Exception as error:
                        db.session.rollback()
                        status_code = 400
                        response_body = {
                            "result": f"HTTP_400_BAD_REQUEST.{type(error)} {error.args}"
                        }
                except Exception as error:
                    status_code = 400
                    response_body = {
                        "result": f"HTTP_400_BAD_REQUEST. {type(error)} {error.args}."
                    }
                
                
            else:
                # producto has 5 images uploaded
                response_body = {
                    "result": "HTTP_404_BAD_REQUEST. No puedes subir mas de 3 imagenes para subir mas debe actualizar a plan basico ."
                }
                status_code = 404

        elif request.method == "DELETE":
            # producto wants to delete a certain image, check id
            # id azul = id de producto // id amarillo = id de productoImage
            if id != 0 and ProductoImage.query.filter_by(id=id).first():
                image_to_delete = ProductoImage.query.filter_by(id=id).first()

                response = uploader.destroy(image_to_delete.public_id)
                if "result" in response and response["result"] == "ok":
                                    
                # url_parts = image_to_delete.image_url.rsplit("/", 2)
                # path_filename = "/".join([url_parts[1], url_parts[2]])
                # if os.path.exists(os.path.join(UPLOAD_FOLDER, path_filename)):
                # os.remove(os.path.join(UPLOAD_FOLDER, path_filename))
                    db.session.delete(image_to_delete)

                    # db.session.commit()
                    # response_body = {
                    #     "result": "HTTP_204_NO_CONTENT. image deleted."
                    # }
                    # status_code = 204
                    try:
                        db.session.commit()
                        response_body = {
                            "result": "HTTP_204_NO_CONTENT. image deleted."
                        }
                        status_code = 204
                    except Exception as error:
                        db.session.rollback()
                        response_body = {
                            "result": f"HTTP_500_INTERNAL_SERVER_ERROR. {type(error)} {error.args}"
                        }                    
                else:
                    response_body = {
                        "result": f"HTTP_404_NOT_FOUND. {response['result'] if 'result' in response else 'image not found...'}"
                    }
                    status_code = 404

        else:
            # bad request method...
            response_body = {
                "result": "HTTP_400_BAD_REQUEST. This is not a valid method for this endpoint."
            }
            status_code = 400
    else:
        # producto doesn't exist
        response_body = {
            "result": "HTTP_400_BAD_REQUEST. cannot handle images for non existing product..."
        }
        status_code = 400

    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )

# static image file serving
@app.route("/src/static/images/<filename>", methods=["GET"])
def serve_image(filename):
    
    secured_filename = secure_filename(filename)
    image_path = os.path.join("images", secured_filename)
    
    if os.path.exists(os.path.join(app.static_folder, image_path)):
        return send_from_directory(app.static_folder, image_path)
    else:
        return "HTTP_404_NOT_FOUND"













































# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)