from flask import Blueprint, request, jsonify
from src.doctor_user.infrastructure.controller import DoctorController
from include.validators import checkArgs, parsedRespond

# Crear un blueprint para el manejo de rutas de usuario
doctor_bp = Blueprint('doctor', __name__)

# Instanciar el controlador de usuario
doctor_controller = DoctorController()

#Funcion de consulta
def consulta(id_doctor):
    doctor_info = doctor_controller.authenticate_doctor(id_doctor)  # Pasar credencial y contraseña
    return parsedRespond(doctor_info)


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@doctor_bp.route('/info', methods=['GET', 'POST'])
def auth_doctor():
    # Aquí puedes manejar ambos métodos, GET o POST
    if request.method == 'GET':
        # Si los parámetros vienen en la URL
        checkArgs(['id_doctor'], request.args)
        id_doctor = request.args['id_doctor']
    elif request.method == 'POST':
        # Si los parámetros vienen en un formulario POST
        id_doctor = request.form.get('id_doctor')

    try:
        # Llamar al método de autenticación del controlador
        return jsonify(consulta(id_doctor)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


