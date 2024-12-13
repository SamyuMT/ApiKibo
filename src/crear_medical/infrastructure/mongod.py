from ...mongo.connect import ConnectionMongo

class MongodCrearMedical:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def CrearMedicalConnect(self):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["medical_info"]
        return col
