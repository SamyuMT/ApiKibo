from flask import Blueprint, request, abort
from src.crear_emergency.infrastructure.controller import CrearEmergencyInfoController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_emergency_bp = Blueprint('crear_emergency', __name__)
emergency_crear_controller = CrearEmergencyInfoController()

# Función de consulta
def consulta(info, id):
    emergency_info = emergency_crear_controller.crear_EmergencyInfo(info, id)  # Pasar información de emergencia y ID

# Definir una ruta POST para crear información de emergencia
@crear_emergency_bp.route('/create', methods=['POST'])
def set_crear_emergency():
    """
    Crear información de emergencia.
    ---
    tags:
      - Crear Usuario
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos necesarios para crear la información de emergencia
        required: true
        schema:
          type: object
          properties:
            id:
              type: string
              example: "user123"
            data:
              type: object
              properties:
                name:
                  type: string
                  example: "John"
                last_name:
                  type: string
                  example: "Doe"
                gender:
                  type: string
                  example: "male"
                type_doc:
                  type: string
                  example: "passport"
                doc_number:
                  type: string
                  example: "123456789"
                cel_mobile:
                  type: string
                  example: "1234567890"
                relationship:
                  type: string
                  example: "friend"
                department:
                  type: string
                  example: "IT"
                city:
                  type: string
                  example: "New York"
                neighborhood:
                  type: string
                  example: "Brooklyn"
                type_street:
                  type: string
                  example: "Avenue"
                street_number:
                  type: string
                  example: "5th"
                house_number:
                  type: string
                  example: "123"
    responses:
      200:
        description: Información de emergencia creada correctamente
      404:
        description: Error al crear
    """
    data = request.get_json()
    info_cre = data.get('data')
    id = data.get('id')
    if not info_cre or not id:
        return abort(400, description="Datos no proporcionados")
    try:
        consulta(info_cre, id)
        return f"Información de emergencia creada correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")