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
    data = request.get_json()
    id = data.get('id')
    ecg = data.get('ecg')
    bpm = data.get('bpm')
    pred = data.get('pred')
    try:
        
        return jsonify(consulta(id,ecg,bpm,pred)), 200
    except FileNotFoundError:
        return abort(404, description="Error al crear")

