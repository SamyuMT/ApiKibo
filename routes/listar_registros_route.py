from flask import Blueprint, jsonify, request, send_file, abort
from src.listar_registros.infrastructure.controller import ListarRegistrosController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
listar_registros_bp = Blueprint('listar_registros', __name__)
listar_registros_controller = ListarRegistrosController()


#Funcion de consulta

def consulta():
    listar_registros = listar_registros_controller.listarRegistros()  # Pasar credencial y contraseña
    return listar_registros


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@listar_registros_bp.route('/info', methods=['GET'])
def set_data_ecg():
    """
    Listar registros de datos.
    ---
    tags:
      - Registros
    produces:
      - application/json
    responses:
      200:
        description: Lista de registros obtenida correctamente
        schema:
          type: array
          items:
            type: object
            properties:
              _id:
                type: string
                example: "id123"
              created_date:
                type: string
                example: "2024-12-31"
              created_time:
                type: string
                example: "17:05:58"
              email:
                type: string
                example: "example1@hotmail.com"
              full_name:
                type: string
                example: "example example"
              id_user:
                type: string
                example: "id123"
              length:
                type: integer
                example: 289
              type:
                type: string
                example: "Pred"
      404:
        description: Error al obtener la lista de registros
    """
    try:
        listaRegistro = consulta()
        return jsonify(listaRegistro), 200
    except FileNotFoundError:
        return abort(404, description="Error al obtener la lista de registros")

