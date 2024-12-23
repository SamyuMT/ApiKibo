from flask import Blueprint, request, abort
from src.crear_doctor.infrastructure.controller import CrearDoctorController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_doctor_bp = Blueprint('crear_doctor', __name__)
doctor_crear_controller = CrearDoctorController()

# Función de consulta
def consulta(info, id):
    doctor_info = doctor_crear_controller.crear_Doctor(info, id)  # Pasar información del doctor y ID

# Definir una ruta POST para crear un doctor
@crear_doctor_bp.route('/create', methods=['POST'])
def set_crear_doctor():
    """
    Crear un nuevo doctor.
    ---
    tags:
      - Doctores
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos necesarios para crear el doctor
        required: true
        schema:
          type: object
          properties:
            id:
              type: string
              example: "doctor123"
            data:
              type: object
              properties:
                name:
                  type: string
                  example: "John"
                last_name:
                  type: string
                  example: "Doe"
                specialty:
                  type: string
                  example: "Cardiology"
                institution:
                  type: string
                  example: "General Hospital"
                email:
                  type: string
                  example: "john.doe@example.com"
    responses:
      200:
        description: Doctor creado correctamente
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
        return f"Doctor creado correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")