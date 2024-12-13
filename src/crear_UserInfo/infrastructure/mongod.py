from ...mongo.connect import ConnectionMongo

class MongodCrearUserInfo:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def CrearUserInfoConnect(self):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["info_user"]
        return col
