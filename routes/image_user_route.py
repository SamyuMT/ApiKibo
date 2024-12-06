from flask import Blueprint, request, send_file, abort
import os

from include.validators import checkArgs

# Crear un blueprint para el manejo de rutas de usuario
image_user_bp = Blueprint('image_user', __name__)


#Funcion de consulta

def consulta(img_url):
    image_folder = 'static/imag_users'
    full_path = os.path.join(image_folder, img_url)
    return send_file(full_path, mimetype='image/jpeg')


# Definir una ruta POST para autenticar usuario (correo o celular + contraseña)
@image_user_bp.route('/img', methods=['GET'])
def get_image_user():
    checkArgs(['img_url'], request.args)
    img_url = request.args['img_url']
    print(img_url)
    try:
        # Llamar al método de autenticación del controlador
        cons = consulta(img_url)
        return cons
        
    except FileNotFoundError:
        return abort(404, description="Image not found")

