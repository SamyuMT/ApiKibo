from ...mongo.connect import ConnectionMongo

class MongodValidarNumber:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def ValidarNumberConnect(self, number):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["credential"]
        info = col.find_one({"cel_mobile": number})
        return info
