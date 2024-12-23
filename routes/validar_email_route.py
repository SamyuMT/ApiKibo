from flask import Blueprint, request, jsonify, abort
from src.validar_email.infrastructure.controller import ValidarEmailController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de usuario
validar_email_bp = Blueprint('validar_email', __name__)

validador_controller = ValidarEmailController()

# Función de consulta
def consulta(email):
    info = validador_controller.authenticate_validar_email(email)  # Pasar credencial y contraseña
    return info

# Definir una ruta GET para validar email
@validar_email_bp.route('/info', methods=['GET'])
def validar_email():
    """
    Validación de email de usuario.
    ---
    tags:
      - Credenciales
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: Email del usuario.
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
              example: "Email no encontrado"
    """
    # Si los parámetros vienen en la URL
    checkArgs(['email'], request.args)
    email = request.args['email']

    try:
        result = consulta(email)
        if result == True:
            # Llamar al método de autenticación del controlador
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return abort(404, description="conexión inestable")