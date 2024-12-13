from ...mongo.connect import ConnectionMongo

class MongodCrearUser:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def CrearUserConnect(self):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["users"]
        return col
