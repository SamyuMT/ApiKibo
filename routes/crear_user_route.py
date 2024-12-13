from flask import Blueprint, request, send_file, abort
from src.crear_user.infrastructure.controller import CrearUserController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_user_bp = Blueprint('crear_user', __name__)
user_crear_controller = CrearUserController()


#Funcion de consulta

def consulta(info, id):
    user_info = user_crear_controller.crear_user(info, id)  # Pasar credencial y contraseña



# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@crear_user_bp.route('/create', methods=['POST'])
def set_crear_user():
    data = request.get_json()
    info_cre = data.get('data')
    id = data.get('id')
    try:
        consulta(info_cre, id)
        return f"Credencial creada correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")

