from ...mongo.connect import ConnectionMongo
from bson.objectid import ObjectId  # Importa ObjectId para consultas por _id


class MongodDoctor:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def DoctorConnect(self, id_doctor):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["doctor_user"]
        if "@" in id_doctor:  # Es un correo electrónico
            doctor = col.find_one({"email": id_doctor})
        else:
            doctor = col.find_one({"_id": ObjectId(id_doctor)})
        return doctor
