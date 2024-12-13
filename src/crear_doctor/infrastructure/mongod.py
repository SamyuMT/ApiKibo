from ...mongo.connect import ConnectionMongo

class MongodCrearDoctor:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def CrearDoctorConnect(self):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["doctor_user"]
        return col
