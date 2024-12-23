from flask import Blueprint, request, jsonify, abort
from src.validar_number.infrastructure.controller import ValidarNumberController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de usuario
validar_number_bp = Blueprint('validar_number', __name__)

validador_controller = ValidarNumberController()

# Función de consulta
def consulta(number):
    info = validador_controller.authenticate_validar_number(number)  # Pasar credencial y contraseña
    return info

# Definir una ruta GET para validar número
@validar_number_bp.route('/info', methods=['GET'])
def validar_number():
    """
    Validación de número de usuario.
    ---
    tags:
      - Credenciales
    parameters:
      - name: number
        in: query
        type: string
        required: true
        description: Número del usuario.
    responses:
      200:
        description: Validación exitosa.
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: boolean
              description: Resultado de la validación.
              example: true
      400:
        description: Error en la validación.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
              example: "Número no encontrado"
    """
    # Si los parámetros vienen en la URL
    checkArgs(['number'], request.args)
    number = request.args['number']

    try:
        result = consulta(number)
        if result == True:
            # Llamar al método de autenticación del controlador
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return abort(404, description="conexión inestable")