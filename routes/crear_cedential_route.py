from flask import Blueprint, request, abort
from src.crear_credential.infrastructure.controller import CrearCredentialController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_credential_bp = Blueprint('crear_credential', __name__)
credential_crear_controller = CrearCredentialController()

# Función de consulta
def consulta(info):
    credential_info = credential_crear_controller.crear_credential(info)  # Pasar credencial y contraseña

# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@crear_credential_bp.route('/create', methods=['POST'])
def set_crear_credential():
    """
    Crear una nueva credencial.
    ---
    tags:
      - Crear Credencial
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos necesarios para crear la credencial
        required: true
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                email:
                  type: string
                  example: "example@example.com"
                cel_number:
                  type: string
                  example: "1234567890"
                id:
                  type: string
                  example: "password123"
    responses:
      200:
        description: Credencial creada correctamente
      404:
        description: Error al crear
    """
    data = request.get_json().get('data')
    if not data:
        return abort(400, description="Datos no proporcionados")
    try:
        consulta(data)
        return f"Credencial creada correctamente {data}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")