from flask import Blueprint, request, jsonify
from src.doctor_user.infrastructure.controller import DoctorController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de doctor
doctor_bp = Blueprint('doctor', __name__)

# Instanciar el controlador de doctor
doctor_controller = DoctorController()

# Función de consulta
def consulta(id_doctor):
    doctor_info = doctor_controller.authenticate_doctor(id_doctor)  # Pasar credencial y contraseña
    return parsedRespond(doctor_info)

# Definir una ruta GET para consultar información de doctor
@doctor_bp.route('/info', methods=['GET'])
def auth_doctor():
    """
    Consulta de información de doctor.
    ---
    tags:
      - Doctores
    parameters:
      - name: id_doctor
        in: query
        type: string
        required: true
        description: ID del doctor.
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
                  description: ID del doctor.
                  example: "D12345"
                name:
                  type: string
                  description: Nombre del doctor.
                  example: "John"
                last_name:
                  type: string
                  description: Apellido del doctor.
                  example: "Doe"
                specialty:
                  type: string
                  description: Especialidad del doctor.
                  example: "Cardiología"
                institution:
                  type: string
                  description: Institución del doctor.
                  example: "Hospital General"
                email:
                  type: string
                  description: Correo electrónico del doctor.
                  example: "doctor@example.com"
                state:
                  type: boolean
                  description: Estado del doctor.
                  example: true
      400:
        description: Error en la consulta.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
              example: "Doctor no encontrado"
    """
    # Si los parámetros vienen en la URL
    checkArgs(['id_doctor'], request.args)
    id_doctor = request.args['id_doctor']

    try:
        # Llamar al método de autenticación del controlador
        return jsonify(consulta(id_doctor)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400