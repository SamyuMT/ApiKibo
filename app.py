from flask import Flask
from flask_cors import CORS
from routes.user_route import user_bp

app = Flask(__name__)
CORS(app)

# Registrar el blueprint de usuario
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
