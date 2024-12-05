from ...mongo.connect import ConnectionMongo

class MongodUserInfo:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def UserInfoConnect(self, id_user):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["info_user"]
        infoUser = col.find_one({"id_user": id_user})
        return infoUser
