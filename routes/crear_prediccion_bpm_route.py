from flask import Blueprint, jsonify, request, send_file, abort
from src.prediccion_bpm.infrastructure.controller import PrediccionController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
prediccion_bpm_bp = Blueprint('prediccionbpm', __name__)
prediccion_controller = PrediccionController()


#Funcion de consulta

def consulta(info):
    infoBpm = prediccion_controller.prediccion(info)  # Pasar credencial y contraseña
    return infoBpm


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@prediccion_bpm_bp.route('/prediccion', methods=['POST'])
def set_prediccion():
    data = request.get_json()
    info = data.get('data')
    try:
        
        return jsonify(consulta(info)), 200
    except FileNotFoundError:
        return abort(404, description="Error al crear")

