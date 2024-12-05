from flask import Blueprint, request, jsonify
from src.credential.infrastructure.controller import CredentialController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de usuario
credential_bp = Blueprint('credential', __name__)

# Instanciar el controlador de usuario
credential_controller = CredentialController()

#Funcion de consulta

def consulta(credential, pasw):
    credential_info = credential_controller.authenticate_credential(credential, pasw)  # Pasar credencial y contraseña
    return parsedRespond(credential_info)


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@credential_bp.route('/login', methods=['GET', 'POST'])
def auth_credential():
    # Aquí puedes manejar ambos métodos, GET o POST
    if request.method == 'GET':
        # Si los parámetros vienen en la URL
        checkArgs(['credential', 'pass'], request.args)
        credential = request.args['credential']
        pasw = request.args['pass']
    elif request.method == 'POST':
        # Si los parámetros vienen en un formulario POST
        credential = request.form.get('credential')
        pasw = request.form.get('password')

    try:
        # Llamar al método de autenticación del controlador
        return jsonify(consulta(credential, pasw)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

