from ...mongo.connect import ConnectionMongo

class MongodCrearEmergencyInfo:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def CrearEmergencyInfoConnect(self):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["emergency_user"]
        return col
