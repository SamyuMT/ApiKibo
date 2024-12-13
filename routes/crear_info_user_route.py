from flask import Blueprint, request, send_file, abort
from src.crear_UserInfo.infrastructure.controller import CrearUserInfoController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_UserInfo_bp = Blueprint('crear_UserInfo', __name__)
UserInfo_crear_controller = CrearUserInfoController()


#Funcion de consulta

def consulta(info, id):
    UserInfo_info = UserInfo_crear_controller.crear_UserInfo(info, id)  # Pasar credencial y contraseña



# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@crear_UserInfo_bp.route('/create', methods=['POST'])
def set_crear_UserInfo():
    data = request.get_json()
    info_cre = data.get('data')
    id = data.get('id')
    try:
        consulta(info_cre, id)
        return f"Credencial creada correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")

