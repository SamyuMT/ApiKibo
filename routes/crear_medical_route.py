from flask import Blueprint, request, abort
from src.crear_medical.infrastructure.controller import CrearMedicalController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_medical_bp = Blueprint('crear_medical', __name__)
medical_crear_controller = CrearMedicalController()

# Función de consulta
def consulta(info, id):
    medical_info = medical_crear_controller.crear_medical(info, id)  # Pasar información médica y ID

# Definir una ruta POST para crear información médica
@crear_medical_bp.route('/create', methods=['POST'])
def set_crear_medical():
    """
    Crear información médica.
    ---
    tags:
      - Crear Medical
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos necesarios para crear la información médica
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
                type_link:
                  type: string
                  example: "primary"
                id_doctor:
                  type: string
                  example: "doctor123"
                insurance:
                  type: string
                  example: "Health Insurance"
    responses:
      200:
        description: Información médica creada correctamente
      404:
        description: Error al crear
    """
    data = request.get_json()
    info_cre = data.get('data')
    id = data.get('id')
    if not info_cre or not id:
        return abort(400, description="Datos no proporcionados")
    try:
        print(info_cre, id)
        consulta(info_cre, id)
        return f"Información médica creada correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")