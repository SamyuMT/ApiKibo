from flask import Blueprint, jsonify, request, send_file, abort
from src.alarma.infrastructure.controller import AlarmaController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
alerta_bp = Blueprint('alerta', __name__)
alarma_controller = AlarmaController()


#Funcion de consulta

def consulta(mensage, latitud, longitud, cel_emergencia, cel_contacto):
    infoBpm = alarma_controller.alarma(mensage, latitud, longitud, cel_emergencia, cel_contacto)  # Pasar credencial y contraseña
    return infoBpm


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@alerta_bp.route('/info', methods=['POST'])
def set_alarma():
    data = request.get_json()
    mensage = data.get('data')
    latitud = data.get('latitud')
    longitud = data.get('longitud')
    cel_emergencia = data.get('cel_emergencia')
    cel_contacto = data.get('cel_contacto')

    resultado = consulta(mensage, latitud, longitud, cel_emergencia, cel_contacto)
    try:
        
        return jsonify(mensage), 200
    except FileNotFoundError:
        return abort(404, description="Error al crear")

