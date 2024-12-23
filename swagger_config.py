from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger
from flask import jsonify

def configure_swagger(app):
    """
    Configura Swagger para la aplicación Flask.
    """
    @app.route('/swagger.json')
    def swagger_spec():
        """
        Genera el archivo Swagger JSON automáticamente desde las rutas de Flask.
        """
        swag = swagger(app)
        swag['info'] = {
            "title": "API Documentation",
            "version": "1.0",
            "description": "Documentación de la API con todas las rutas registradas"
        }
        return jsonify(swag)

    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL,
        config={'app_name': "Flask API"}
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)