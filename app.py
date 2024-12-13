from flask import Flask
from flask_cors import CORS
from routes.credential_route import credential_bp
from routes.user_route import user_bp
from routes.user_info_route import user_info_bp
from routes.user_emergency_route import user_emergency_bp
from routes.medical_info_route import medical_info_bp
from routes.doctor_route import doctor_bp
from routes.image_user_route import image_user_bp
from routes.validar_email_route import validar_email_bp
from routes.validar_number_route import validar_number_bp
from routes.crear_cedential_route import crear_credential_bp
from routes.crear_user_route import crear_user_bp
from routes.crear_info_user_route import crear_UserInfo_bp
from routes.crear_user_emergency_route import crear_emergency_bp
from routes.crear_doctor_route import crear_doctor_bp
from routes.crear_medical_route import crear_medical_bp


app = Flask(__name__)
CORS(app)

# Registrar el blueprint de usuario
app.register_blueprint(credential_bp, url_prefix='/get_credential')
app.register_blueprint(user_bp,url_prefix='/get_user')
app.register_blueprint(user_info_bp,url_prefix='/get_user_info')
app.register_blueprint(user_emergency_bp,url_prefix='/get_user_emergency')
app.register_blueprint(medical_info_bp,url_prefix='/get_medical_info')
app.register_blueprint(doctor_bp,url_prefix='/get_doctor')
app.register_blueprint(image_user_bp,url_prefix='/get_image_user')
app.register_blueprint(validar_email_bp,url_prefix='/get_validar_email')
app.register_blueprint(validar_number_bp,url_prefix='/get_validar_number')
app.register_blueprint(crear_credential_bp,url_prefix='/set_credential')
app.register_blueprint(crear_user_bp,url_prefix='/set_user')
app.register_blueprint(crear_UserInfo_bp,url_prefix='/set_user_info')
app.register_blueprint(crear_emergency_bp,url_prefix='/set_emergency_info')
app.register_blueprint(crear_doctor_bp,url_prefix='/set_doctor')
app.register_blueprint(crear_medical_bp,url_prefix='/set_medical')


@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
