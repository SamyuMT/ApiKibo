from ...mongo.connect import ConnectionMongo

class MongodMedicalInfo:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def MedicalInfoConnect(self, id_user):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["medical_info"]
        user = col.find_one({"id_user": id_user})
        return user
