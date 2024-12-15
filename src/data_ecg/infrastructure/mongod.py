from ...mongo.connect import ConnectionMongo

class MongodDataEcg:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def DataEcgConnect(self):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col_pred = db["data_pred"]
        col_bpm = db["data_bpm"]
        col_ecg = db["data_ecg"]
        return col_ecg,col_bpm,col_pred
