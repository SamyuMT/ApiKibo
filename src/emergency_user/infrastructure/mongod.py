from ...mongo.connect import ConnectionMongo

class MongodUserEmergency:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def UserEmergencyConnect(self, id_user):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["emergency_user"]
        infoUser = col.find_one({"id_user": id_user})
        return infoUser
