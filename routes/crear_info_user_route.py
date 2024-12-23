from flask import Blueprint, request, abort
from src.crear_UserInfo.infrastructure.controller import CrearUserInfoController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_UserInfo_bp = Blueprint('crear_UserInfo', __name__)
UserInfo_crear_controller = CrearUserInfoController()

# Función de consulta
def consulta(info, id):
    UserInfo_info = UserInfo_crear_controller.crear_UserInfo(info, id)  # Pasar información del usuario y ID

# Definir una ruta POST para crear información de usuario
@crear_UserInfo_bp.route('/create', methods=['POST'])
def set_crear_UserInfo():
    """
    Crear información de usuario.
    ---
    tags:
      - Crear Usuario
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos necesarios para crear la información del usuario
        required: true
        schema:
          type: object
          properties:
            id:
              type: string
              example: "user123"
            data:
              type: object
              properties:
                gender:
                  type: string
                  example: "male"
                type_doc:
                  type: string
                  example: "passport"
                doc_number:
                  type: string
                  example: "123456789"
                department:
                  type: string
                  example: "IT"
                city:
                  type: string
                  example: "New York"
                neighborhood:
                  type: string
                  example: "Brooklyn"
                type_street:
                  type: string
                  example: "Avenue"
                street_number:
                  type: string
                  example: "5th"
                house_number:
                  type: string
                  example: "123"
    responses:
      200:
        description: Información de usuario creada correctamente
      404:
        description: Error al crear
    """
    data = request.get_json()
    info_cre = data.get('data')
    id = data.get('id')
    if not data or not id:
        return abort(400, description="Datos no proporcionados")
    try:
        consulta(info_cre, id)
        return f"Información de usuario creada correctamente {info_cre}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")