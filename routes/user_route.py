from flask import Blueprint, request, jsonify
from include.validators import checkArgs, parsedRespond
from src.user.infrastructure.controller import UserController

# Crear un blueprint para el manejo de rutas de usuario
user_bp = Blueprint('user', __name__)

# Instanciar el controlador de usuario
user_controller = UserController()

#Funcion de consulta

def consulta(creditial, pasw):
    user_info = user_controller.authenticate_user(creditial, pasw)  # Pasar credencial y contraseña
    return parsedRespond(user_info)


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@user_bp.route('/login', methods=['GET', 'POST'])
def auth_user():
    # Aquí puedes manejar ambos métodos, GET o POST
    if request.method == 'GET':
        # Si los parámetros vienen en la URL
        checkArgs(['credential', 'pass'], request.args)
        creditial = request.args['credential']
        pasw = request.args['pass']
    elif request.method == 'POST':
        # Si los parámetros vienen en un formulario POST
        creditial = request.form.get('credential')
        pasw = request.form.get('password')

    try:
        # Llamar al método de autenticación del controlador
        return jsonify(consulta(creditial, pasw)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

