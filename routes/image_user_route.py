from flask import Blueprint, request, send_file, abort
import os

from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
image_user_bp = Blueprint('image_user', __name__)

# Función de consulta
def consulta(img_url):
    image_folder = 'static/imag_users'
    full_path = os.path.join(image_folder, img_url)
    return send_file(full_path, mimetype='image/jpeg')

# Definir una ruta GET para obtener la imagen de usuario
@image_user_bp.route('/img', methods=['GET'])
def get_image_user():
    """
    Obtención de imagen de usuario.
    ---
    tags:
      - Usuarios
    parameters:
      - name: img_url
        in: query
        type: string
        required: true
        description: URL de la imagen del usuario.
    responses:
      200:
        description: Imagen obtenida exitosamente.
        content:
          image/jpeg:
            schema:
              type: string
              format: binary
      404:
        description: Imagen no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
              example: "Image not found"
    """
    checkArgs(['img_url'], request.args)
    img_url = request.args['img_url']
    print(img_url)
    try:
        # Llamar al método de consulta
        cons = consulta(img_url)
        return cons
    except FileNotFoundError:
        return abort(404, description="Image not found")