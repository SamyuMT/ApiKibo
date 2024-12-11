from flask import Blueprint, request, jsonify, abort
from src.validar_email.infrastructure.controller import ValidarEmailController
from include.validators import checkArgs, parsedRespond
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
validar_email_bp = Blueprint('validar_email', __name__)


validador_controller = ValidarEmailController()


#Funcion de consulta
def consulta(email):
    info = validador_controller.authenticate_validar_email(email)  # Pasar credencial y contraseña
    return info


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@validar_email_bp.route('/info', methods=['GET', 'POST'])
def validar_email():
    # Aquí puedes manejar ambos métodos, GET o POST
    if request.method == 'GET':
        # Si los parámetros vienen en la URL
        checkArgs(['email'], request.args)
        email = request.args['email']
    elif request.method == 'POST':
        # Si los parámetros vienen en un formulario POST
        email = request.form.get('email')

    try:
        result = consulta(email)
        if result == True:
        # Llamar al método de autenticación del controlador
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return abort(404, description="conexión inestable")

