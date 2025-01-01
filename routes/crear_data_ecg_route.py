from flask import Blueprint, jsonify, request, send_file, abort
from src.data_ecg.infrastructure.controller import DataEcgController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_data_ecg_bp = Blueprint('crear_data_ecg', __name__)
data_ecg_controller = DataEcgController()


#Funcion de consulta

def consulta(id,ecg,bpm,pred):
    infoBpm = data_ecg_controller.data_ecg(id,ecg,bpm,pred)  # Pasar credencial y contraseña
    return infoBpm


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@crear_data_ecg_bp.route('/info', methods=['POST'])
def set_data_ecg():
    """
    Guardar Data de interes.
    ---
    tags:
      - Guardar Data
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos necesarios para guardar data de interes
        required: true
        schema:
          type: object
          properties:
            id:
              type: string
              example: "6774504f59bdd3a54dd87a5e"
            ecg:
              type: array
              items:
                type: number
              example: [0.1, 0.2, 0.3, 0.4, 0.5]
            bpm:
              type: array
              items:
                type: number
              example: [89, 100, 98, 70]
            pred:
              type: array
              items:
                type: string
              example: ["V", "f", "F", "N"]
    responses:
      200:
        description: Información de ECG creada correctamente
      404:
        description: Error al crear
    """
    data = request.get_json()
    id = data.get('id')
    ecg = data.get('ecg')
    bpm = data.get('bpm')
    pred = data.get('pred')
    try:
        
        return jsonify(consulta(id,ecg,bpm,pred)), 200
    except FileNotFoundError:
        return abort(404, description="Error al crear")

