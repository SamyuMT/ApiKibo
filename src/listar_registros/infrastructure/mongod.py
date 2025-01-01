from ...mongo.connect import ConnectionMongo
from bson import ObjectId

class MongodListarRegistros:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def ListarRegistrosConnect(self):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col_pred = db["data_pred"]
        col_bpm = db["data_bpm"]
        col_ecg = db["data_ecg"]
        col_credential = db["credential"]
        col_user = db["users"]

        registros_pred = list(col_pred.find({}, {"data": 0}))
        registros_bpm = list(col_bpm.find({}, {"data": 0}))
        registros_ecg = list(col_ecg.find({}, {"data": 0}))

        for registro in registros_pred:
            registro["type"] = "Pred"
        for registro in registros_bpm:
            registro["type"] = "BPM"
        for registro in registros_ecg:
            registro["type"] = "ECG"
        
        registros = registros_pred + registros_bpm + registros_ecg
        
        for registro in registros:
            id_user = registro["id_user"]
            credential = col_credential.find_one({"_id": ObjectId(id_user)})
            user = col_user.find_one({"id_user": id_user}, {"name": 1, "last_name": 1, "_id": 0})
            if credential:
                registro["email"] = credential["email"]
            if user:
                first_name = user["name"].split()[0]
                first_last_name = user["last_name"].split()[0]
                registro["full_name"] = f"{first_name} {first_last_name}"
            registro["_id"] = str(registro["_id"])

        return registros