from flask import Blueprint, request, jsonify
from src.user.infrastructure.controller import UserController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de usuario
user_bp = Blueprint('user', __name__)

# Instanciar el controlador de usuario
user_controller = UserController()

# Función de consulta
def consulta(id_user):
    user_info = user_controller.authenticate_user(id_user)  # Pasar credencial y contraseña
    return parsedRespond(user_info)

# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@user_bp.route('/info', methods=['GET'])
def auth_user():
    """
    Consulta de información de usuario.
    ---
    tags:
      - Usuarios
    parameters:
      - name: id_user
        in: query
        type: string
        required: true
        description: ID del usuario.
    responses:
      200:
        description: Consulta exitosa.
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: object
              properties:
                id:
                  type: string
                  description: ID del usuario.
                  example: "12345"
                rol:
                  type: string
                  description: Rol del usuario.
                  example: "admin"
                nick_name:
                  type: string
                  description: Apodo del usuario.
                  example: "jdoe"
                name:
                  type: string
                  description: Nombre del usuario.
                  example: "John"
                last_name:
                  type: string
                  description: Apellido del usuario.
                  example: "Doe"
                img_url:
                  type: string
                  description: URL de la imagen del usuario.
                  example: "http://example.com/image.jpg"
                state:
                  type: boolean
                  description: Estado del usuario.
                  example: true
      400:
        description: Error en la consulta.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
              example: "Usuario no encontrado"
    """
    # Si los parámetros vienen en la URL
    checkArgs(['id_user'], request.args)
    id_user = request.args['id_user']

    try:
        # Llamar al método de autenticación del controlador
        return jsonify(consulta(id_user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400