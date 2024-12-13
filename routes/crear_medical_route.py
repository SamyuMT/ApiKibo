from flask import Blueprint, request, send_file, abort
from src.crear_medical.infrastructure.controller import CrearMedicalController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_medical_bp = Blueprint('crear_medical', __name__)
medical_crear_controller = CrearMedicalController()


#Funcion de consulta

def consulta(info, id):
    medical_info = medical_crear_controller.crear_medical(info, id)  # Pasar credencial y contraseña



# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@crear_medical_bp.route('/create', methods=['POST'])
def set_crear_medical():
    data = request.get_json()
    info_cre = data.get('data')
    id = data.get('id')
    try:
        consulta(info_cre, id)
        return f"Credencial creada correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")

