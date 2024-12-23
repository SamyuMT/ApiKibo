from flask import Blueprint, jsonify, request, send_file, abort
from src.alarma.infrastructure.controller import AlarmaController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
alerta_bp = Blueprint('alerta', __name__)
alarma_controller = AlarmaController()


#Funcion de consulta

def consulta(mensage, latitud, longitud, cel_emergencia, cel_contacto, account_sid, auth_token):
    infoBpm = alarma_controller.alarma(mensage, latitud, longitud, cel_emergencia, cel_contacto, account_sid, auth_token)  # Pasar credencial y contraseña
    return infoBpm


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@alerta_bp.route('/info', methods=['POST'])
def set_alarma():
    """
    Crear una nueva alerta.
    ---
    tags:
      - Crear Alerta
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos necesarios para crear la alerta
        required: true
        schema:
          type: object
          properties:
            data:
              type: string
              example: "Alerta de prueba"
            latitud:
              type: string
              example: "4.60971"
            longitud:
              type: string
              example: "-74.08175"
            cel_emergencia:
              type: string
              example: "1234567890"
            cel_contacto:
              type: string
              example: "0987654321"
            account_sid:
              type: string
              example: "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            auth_token:
              type: string
              example: "your_auth_token"
    responses:
      200:
        description: Alerta creada correctamente
      404:
        description: Error al crear
    """
    data = request.get_json()
    mensage = data.get('data')
    latitud = data.get('latitud')
    longitud = data.get('longitud')
    cel_emergencia = data.get('cel_emergencia')
    cel_contacto = data.get('cel_contacto')
    account_sid = data.get('account_sid')
    auth_token = data.get('auth_token')

    resultado = consulta(mensage, latitud, longitud, cel_emergencia, cel_contacto, account_sid, auth_token)
    try:
        
        return jsonify(mensage), 200
    except FileNotFoundError:
        return abort(404, description="Error al crear")

