from src.crear_user.infrastructure.mongod import MongodCrearUser
from ..application.response import CrearUserResponse

class CrearUserController:

    def __init__(self):
        self.mongo_number_validar = MongodCrearUser()
        self.response = CrearUserResponse()

    def crear_user(self, data, id):
        col = self.mongo_number_validar.CrearUserConnect()
        parsed = self.response.SetCrearUser(col, data, id)
        return parsed


