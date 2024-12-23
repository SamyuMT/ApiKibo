from flask import Blueprint, request, abort
from src.crear_user.infrastructure.controller import CrearUserController
from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
crear_user_bp = Blueprint('crear_user', __name__)
user_crear_controller = CrearUserController()

# Función de consulta
def consulta(info, id):
    user_info = user_crear_controller.crear_user(info, id)  # Pasar información del usuario y ID

# Definir una ruta POST para crear un usuario
@crear_user_bp.route('/create', methods=['POST'])
def set_crear_user():
    """
    Crear un nuevo usuario.
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
        description: Datos necesarios para crear el usuario
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
                rol:
                  type: string
                  example: "admin"
                nick_name:
                  type: string
                  example: "nickname"
                name:
                  type: string
                  example: "John"
                last_name:
                  type: string
                  example: "Doe"
                img_url:
                  type: string
                  example: "http://example.com/image.jpg"
    responses:
      200:
        description: Usuario creado correctamente
      404:
        description: Error al crear
    """
    json_data = request.get_json()
    id = json_data.get('id')
    data = json_data.get('data')
    if not data or not id:
        return abort(400, description="Datos no proporcionados")
    try:
        consulta(data, id)
        return f"Usuario creado correctamente {data}"
    except FileNotFoundError:
        return abort(404, description="Error al crear")