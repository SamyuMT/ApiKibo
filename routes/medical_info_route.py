from flask import Blueprint, request, jsonify
from src.medical_info.infrastructure.controller import MedicalInfoController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de usuario
medical_info_bp = Blueprint('medical_info', __name__)

# Instanciar el controlador de usuario
medical_info_controller = MedicalInfoController()

#Funcion de consulta
def consulta(id_user):
    medical_info = medical_info_controller.authenticate_medical_info(id_user)  # Pasar credencial y contraseña
    return parsedRespond(medical_info)


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@medical_info_bp.route('/info', methods=['GET', 'POST'])
def auth_medical_info():
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


