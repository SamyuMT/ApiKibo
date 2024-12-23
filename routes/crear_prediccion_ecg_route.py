from flask import Blueprint, jsonify, request, send_file, abort
from src.prediccion_ecg.infrastructure.controller import PrediccionController
import os
import tensorflow as tf



# Crear un blueprint para el manejo de rutas de usuario
prediccion_ecg_bp = Blueprint('prediccion_ecg', __name__)
prediccion_controller = PrediccionController()

pathModelo = f"{os.getcwd()}/routes/model/model.h5"

# Deshabilitar GPU para TensorFlow
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


# Inicialización del modelo al cargar el blueprint (se carga una sola vez)
try:
    # Cargar el modelo en la CPU
    with tf.device('/CPU:0'):
        model = tf.keras.models.load_model(pathModelo)
    print("Modelo de IA cargado exitosamente en CPU.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None


def consulta(info, model):
    infoEcg = prediccion_controller.prediccion(info, model)  # Pasar credencial y contraseña
    return infoEcg


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@prediccion_ecg_bp.route('/prediccion', methods=['POST'])
def set_prediccion():
    """
    Obtener predicción de ECG.
    ---
    tags:
      - Predicciones
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos necesarios para obtener la predicción de ECG
        required: true
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: number
              example: [0.025721,0.072154,0.102611,0.109784,0.118109,0.203648,0.291746,0.269744,0.192802,0.165047,0.225068,0.287616,0.222322,0.117957,0.065566,0.030505,0.012092,0.001085,0.00822,0.020124,-0.000602,-0.02354,-0.037919,-0.013712,0.001564,-0.034232,-0.07485,-0.037216,0.199939,0.604071,0.814839,0.962701,1.349064,1.15306,0.034956,-0.818533,-1.111957,-1.256089,-1.281121,-1.256048,-1.184679,-0.951194,-0.548781,-0.232686,-0.096677,-0.047459,-0.016757,0.02497,0.044696,0.030863,0.007686,-0.008395,-0.01554,-0.052697,-0.102009,-0.137565,-0.158914,-0.206504,-0.242048,-0.255941,-0.251159,-0.280117,-0.295287,-0.268584,-0.223801,-0.190406,-0.166423,-0.119135,-0.033531,0.018572,0.039004,0.056992,0.101329,0.136995,0.129995,0.118068,0.136092,0.153613,0.152733,0.132125,0.115496,0.115455,0.108447,0.096438,0.091158,0.095386,0.074111,0.045268,0.046327,0.074547,0.074438,0.057126,0.055743,0.062951,0.074096,0.06535,0.044606,0.058689,0.070307,0.057938,0.055045,0.066308,0.080099,0.088266,0.117417,0.136988,0.180567,0.199503,0.249251,0.301052,0.286408,0.224583,0.212527,0.266763,0.308605,0.238414,0.138154,0.092823,0.075607,0.050585,0.020167,0.004963,0.025001,0.036128,0.02406,0.008493,0.020379,0.040652,0.043503,0.028969,0.053487,0.238479,0.668559,0.958527,1.032546,1.324524,1.281201,0.22107,-0.830889,-1.159392,-1.284992,-1.344033,-1.323877,-1.217791,-1.015669,-0.655207,-0.29262,-0.098588,-0.027354,0.004454,0.009695,0.014818,0.031039,0.015571,-0.027367,-0.050544,-0.051879,-0.085406,-0.126217,-0.151405,-0.171196,-0.196059,-0.249479,-0.283843,-0.276935,-0.306693,-0.323945,-0.323686,-0.291089,-0.244527,-0.224321,-0.205319,-0.132484,-0.060861,-0.028902,-0.015188,0.021207,0.062599,0.090536,0.104449,0.117154,0.128003,0.111483,0.092518,0.096074,0.106236,0.094176,0.069256,0.075986,0.095845,0.087607,0.056015,0.039151,0.051311,0.066355,0.049656,0.031056,0.04473,0.061651,0.065895,0.056562,0.057478,0.062544,0.064692,0.054272,0.056436,0.072818,0.072101,0.070096,0.089447,0.126801,0.147511,0.155558,0.185649,0.270253,0.317442,0.268481,0.207829,0.249373,0.312687,0.258941,0.15087,0.103818,0.08727,0.043743,0.017038,0.018176,0.037703,0.040498,0.024064,0.012167,0.024766,0.030541,0.030851,0.003161,0.013746,0.219984,0.649734,0.942531,0.99632,1.24589,1.459853,0.765058,-0.396708,-0.950649,-1.135322,-1.237874,-1.253447,-1.201469,-1.068227,-0.741678,-0.311085,-0.073198,-0.015669,-0.003494,0.013435,0.03095,0.027809,0.011865,-0.008783,-0.024965,-0.050161,-0.103131,-0.142376,-0.150125,-0.184766,-0.23444,-0.266754,-0.272153,-0.287456,-0.325877,-0.333778,-0.303521,-0.260674,-0.234784,-0.212146,-0.140763,-0.060936,-0.016971,0.005859,0.048251,0.083649,0.108156,0.121391,0.126015,0.126356,0.122923,0.112012,0.113229,0.126805,0.126008]
    responses:
      200:
        description: Predicción obtenida correctamente
      404:
        description: Error al obtener la predicción
    """
    data = request.get_json()
    info = data.get('data')
    try:
        prediccion = consulta(info, model)
        return jsonify(prediccion), 200
    except FileNotFoundError:
        return abort(404, description="Error al crear")

