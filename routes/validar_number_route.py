from flask import Blueprint, request, jsonify, abort
from src.validar_number.infrastructure.controller import ValidarNumberController
from include.validators import checkArgs
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
validar_number_bp = Blueprint('validar_number', __name__)


validador_controller = ValidarNumberController()


#Funcion de consulta
def consulta(number):
    info = validador_controller.authenticate_validar_number(number)  # Pasar credencial y contraseña
    return info


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@validar_number_bp.route('/info', methods=['GET', 'POST'])
def validar_number():
    # Aquí puedes manejar ambos métodos, GET o POST
    if request.method == 'GET':
        # Si los parámetros vienen en la URL
        checkArgs(['number'], request.args)
        number = request.args['number']
    elif request.method == 'POST':
        # Si los parámetros vienen en un formulario POST
        number = request.form.get('number')

    try:
        result = consulta(number)
        if result == True:
        # Llamar al método de autenticación del controlador
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return abort(404, description="conexión inestable")

