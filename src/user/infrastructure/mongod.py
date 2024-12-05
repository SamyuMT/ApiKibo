from ...mongo.connect import ConnectionMongo

class MongodUser:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def UserConnect(self, id_user):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["users"]
        user = col.find_one({"id_user": id_user})
        return user
