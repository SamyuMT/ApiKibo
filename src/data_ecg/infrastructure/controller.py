from src.data_ecg.infrastructure.mongod import MongodDataEcg
from ..application.response import DataEcgResponse

class DataEcgController:

    def __init__(self):
        self.mongo_number_validar = MongodDataEcg()
        self.response = DataEcgResponse()

    def data_ecg(self, id,ecg,bpm,pred):
        col_ecg,col_bpm,col_pred = self.mongo_number_validar.DataEcgConnect()
        parsed = self.response.SetDataEcg(col_ecg,col_bpm,col_pred,id,ecg,bpm,pred)
        return parsed


