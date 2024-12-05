from flask import Flask
from flask_cors import CORS
from routes.credential_route import credential_bp
from routes.user_route import user_bp
from routes.user_info_route import user_info_bp
from routes.user_emergency_route import user_emergency_bp
from routes.medical_info_route import medical_info_bp
from routes.doctor_route import doctor_bp

app = Flask(__name__)
CORS(app)

# Registrar el blueprint de usuario
app.register_blueprint(credential_bp, url_prefix='/get_credential')
app.register_blueprint(user_bp,url_prefix='/get_user')
app.register_blueprint(user_info_bp,url_prefix='/get_user_info')
app.register_blueprint(user_emergency_bp,url_prefix='/get_user_emergency')
app.register_blueprint(medical_info_bp,url_prefix='/get_medical_info')
app.register_blueprint(doctor_bp,url_prefix='/get_doctor')

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
