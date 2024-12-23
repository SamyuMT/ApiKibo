from flask import Blueprint, request, jsonify
from src.medical_info.infrastructure.controller import MedicalInfoController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de información médica de usuario
medical_info_bp = Blueprint('medical_info', __name__)

# Instanciar el controlador de información médica de usuario
medical_info_controller = MedicalInfoController()

# Función de consulta
def consulta(id_user):
    medical_info = medical_info_controller.authenticate_medical_info(id_user)  # Pasar credencial y contraseña
    return parsedRespond(medical_info)

# Definir una ruta GET para consultar información médica de usuario
@medical_info_bp.route('/info', methods=['GET'])
def auth_medical_info():
    """
    Consulta de información médica de usuario.
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
                insurance:
                  type: string
                  description: Seguro del usuario.
                  example: "Seguro Social"
                type_link:
                  type: string
                  description: Tipo de vínculo del usuario.
                  example: "Titular"
                id_doctor:
                  type: string
                  description: ID del doctor del usuario.
                  example: "D12345"
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
              example: "informacion no encontrado"
    """
    # Si los parámetros vienen en la URL
    checkArgs(['id_user'], request.args)
    id_user = request.args['id_user']

    try:
        # Llamar al método de autenticación del controlador
        return jsonify(consulta(id_user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400