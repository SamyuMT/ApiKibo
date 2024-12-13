from src.crear_UserInfo.infrastructure.mongod import MongodCrearUserInfo
from ..application.response import CrearUserInfoResponse

class CrearUserInfoController:

    def __init__(self):
        self.mongo_number_validar = MongodCrearUserInfo()
        self.response = CrearUserInfoResponse()

    def crear_UserInfo(self, data, id):
        col = self.mongo_number_validar.CrearUserInfoConnect()
        parsed = self.response.SetCrearUserInfo(col, data, id)
        return parsed


