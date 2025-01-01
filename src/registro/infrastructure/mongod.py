from ...mongo.connect import ConnectionMongo
from bson import ObjectId

class MongodRegistro:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def RegistroConnect(self, id, type):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col_pred = db["data_pred"]
        col_bpm = db["data_bpm"]
        col_ecg = db["data_ecg"]


        if type == "Pred":
            registro = col_pred.find_one({"_id": ObjectId(id)}, {"data": 1, "_id": 0})  # Busca el registro con el id especificado y solo trae el campo "data"
        elif type == "BPM":
            registro = col_bpm.find_one({"_id": ObjectId(id)}, {"data": 1, "_id": 0})  # Busca el registro con el id especificado y solo trae el campo "data"
        elif type == "ECG":
            registro = col_ecg.find_one({"_id": ObjectId(id)}, {"data": 1, "_id": 0})  # Busca el registro con el id especificado y solo trae el campo "data"

        if registro:
            registros = registro.get("data", [])
        else:
            registros = []
        return registros