from flask import Blueprint, request, send_file, abort
from src.crear_doctor.infrastructure.controller import CrearDoctorController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_doctor_bp = Blueprint('crear_doctor', __name__)
doctor_crear_controller = CrearDoctorController()


#Funcion de consulta

def consulta(info, id):
    doctor_info = doctor_crear_controller.crear_Doctor(info, id)  # Pasar credencial y contraseña



# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@crear_doctor_bp.route('/create', methods=['POST'])
def set_crear_doctor():
    data = request.get_json()
    info_cre = data.get('data')
    id = data.get('id')
    try:
        consulta(info_cre, id)
        return f"Credencial creada correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")

