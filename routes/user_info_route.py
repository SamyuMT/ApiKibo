from flask import Blueprint, request, jsonify
from src.info_user.infrastructure.controller import UserInfoController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de información de usuario
user_info_bp = Blueprint('user_info', __name__)

# Instanciar el controlador de información de usuario
user_info_controller = UserInfoController()

# Función de consulta
def consulta(id_user):
    user_info = user_info_controller.authenticate_user_info(id_user)  # Pasar credencial y contraseña
    return parsedRespond(user_info)

# Definir una ruta GET para consultar información de usuario
@user_info_bp.route('/info', methods=['GET'])
def auth_info_user():
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
                gender:
                  type: string
                  description: Género del usuario.
                  example: "male"
                type_doc:
                  type: string
                  description: Tipo de documento del usuario.
                  example: "DNI"
                doc_number:
                  type: string
                  description: Número de documento del usuario.
                  example: "12345678"
                department:
                  type: string
                  description: Departamento del usuario.
                  example: "Lima"
                city:
                  type: string
                  description: Ciudad del usuario.
                  example: "Lima"
                neighborhood:
                  type: string
                  description: Barrio del usuario.
                  example: "Miraflores"
                type_street:
                  type: string
                  description: Tipo de calle del usuario.
                  example: "Avenida"
                street_number:
                  type: string
                  description: Número de calle del usuario.
                  example: "123"
                house_number:
                  type: string
                  description: Número de casa del usuario.
                  example: "456"
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