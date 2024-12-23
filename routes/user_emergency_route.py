from flask import Blueprint, request, jsonify
from src.emergency_user.infrastructure.controller import UserEmergencyController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de emergencia de usuario
user_emergency_bp = Blueprint('emergency', __name__)

# Instanciar el controlador de emergencia de usuario
user_emergency_controller = UserEmergencyController()

# Función de consulta
def consulta(id_user):
    user_info = user_emergency_controller.authenticate_user_emergency(id_user)  # Pasar credencial y contraseña
    return parsedRespond(user_info)

# Definir una ruta GET para consultar información de emergencia de usuario
@user_emergency_bp.route('/info', methods=['GET'])
def auth_user_emergency():
    """
    Consulta de información de emergencia de usuario.
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
                name:
                  type: string
                  description: Nombre del usuario.
                  example: "John"
                last_name:
                  type: string
                  description: Apellido del usuario.
                  example: "Doe"
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
                cel_mobile:
                  type: string
                  description: Número de celular del usuario.
                  example: "+1234567890"
                relationship:
                  type: string
                  description: Relación del usuario.
                  example: "Friend"
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