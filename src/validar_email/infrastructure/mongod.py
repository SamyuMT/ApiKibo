from ...mongo.connect import ConnectionMongo

class MongodValidarEmail:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def ValidarEmailConnect(self, email):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["credential"]
        info = col.find_one({"email": email})
        return info
