from flask import Blueprint, jsonify, request, send_file, abort
from src.prediccion_ecg.infrastructure.controller import PrediccionController
import os
import pickle



# Crear un blueprint para el manejo de rutas de usuario
prediccion_ecg_bp = Blueprint('prediccion_ecg', __name__)
prediccion_controller = PrediccionController()

pathModelo = f"{os.getcwd()}/routes/model/model.pkl"

# Inicialización del modelo al cargar el blueprint (se carga una sola vez)
try:
    with open(pathModelo, 'rb') as file:
        model = pickle.load(file)
    print("Modelo de IA cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None

def consulta(info, model):
    infoEcg = prediccion_controller.prediccion(info, model)  # Pasar credencial y contraseña
    return infoEcg


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@prediccion_ecg_bp.route('/prediccion', methods=['POST'])
def set_prediccion():
    data = request.get_json()
    info = data.get('data')
    try:
        prediccion = consulta(info, model)
        return jsonify(prediccion), 200
    except FileNotFoundError:
        return abort(404, description="Error al crear")

