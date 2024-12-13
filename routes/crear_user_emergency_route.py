from flask import Blueprint, request, send_file, abort
from src.crear_emergency.infrastructure.controller import CrearEmergencyInfoController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_emergency_bp = Blueprint('crear_emergency', __name__)
emergency_crear_controller = CrearEmergencyInfoController()


#Funcion de consulta

def consulta(info, id):
    emergency_info = emergency_crear_controller.crear_EmergencyInfo(info, id)  # Pasar credencial y contraseña



# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@crear_emergency_bp.route('/create', methods=['POST'])
def set_crear_emergency():
    data = request.get_json()
    info_cre = data.get('data')
    id = data.get('id')
    try:
        consulta(info_cre, id)
        return f"Credencial creada correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")

