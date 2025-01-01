from flask import Blueprint, jsonify, request, send_file, abort
from src.registro.infrastructure.controller import RegistroController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
registro_route_bp = Blueprint('registro_route', __name__)
registro_route_controller = RegistroController()


#Funcion de consulta

def consulta(id, type):
    registro_route = registro_route_controller.registro(id, type)  # Pasar credencial y contraseña
    return registro_route


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@registro_route_bp.route('/info', methods=['GET'])
def set_data_ecg():
    """
    Traer registro de datos.
    ---
    tags:
      - Registros
    parameters:
      - name: id
        in: query
        type: string
        required: true
        description: requiere un id del registro.
      - name: type
        in: query
        type: string
        required: true
        description: requiere un tipo de registro.
    responses:
      200:
        description: Autenticación exitosa.
      400:
        description: Error de autenticación.
    """
    # Si los parámetros vienen en la URL
    checkArgs(['id', 'type'], request.args)
    id = request.args['id']
    type = request.args['type']
    print(id, type) 
    try:
        #listaRegistro = consulta()
        return jsonify(consulta(id, type)), 200
    except FileNotFoundError:
        return abort(404, description="Error al crear")

