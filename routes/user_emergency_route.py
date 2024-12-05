from flask import Blueprint, request, jsonify
from src.emergency_user.infrastructure.controller import UserEmergencyController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de usuario
user_emergency_bp = Blueprint('emergency', __name__)

# Instanciar el controlador de usuario
user_emergency_controller = UserEmergencyController()

#Funcion de consulta
def consulta(id_user):
    user_info = user_emergency_controller.authenticate_user_emergency(id_user)  # Pasar credencial y contraseña
    return parsedRespond(user_info)


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@user_emergency_bp.route('/info', methods=['GET', 'POST'])
def auth_user_emergency():
    # Aquí puedes manejar ambos métodos, GET o POST
    if request.method == 'GET':
        # Si los parámetros vienen en la URL
        checkArgs(['id_user'], request.args)
        id_user = request.args['id_user']
    elif request.method == 'POST':
        # Si los parámetros vienen en un formulario POST
        id_user = request.form.get('id_user')

    try:
        # Llamar al método de autenticación del controlador
        return jsonify(consulta(id_user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


