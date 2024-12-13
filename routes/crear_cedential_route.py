from flask import Blueprint, request, send_file, abort
from src.crear_credential.infrastructure.controller import CrearCredentialController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_credential_bp = Blueprint('crear_credential', __name__)
credential_crear_controller = CrearCredentialController()


#Funcion de consulta

def consulta(info):
    credential_info = credential_crear_controller.crear_credential(info)  # Pasar credencial y contraseña



# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@crear_credential_bp.route('/create', methods=['POST'])
def set_crear_credential():
    data = request.get_json()
    info_cre = data.get('data')
    try:
        consulta(info_cre)
        return f"Credencial creada correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")

