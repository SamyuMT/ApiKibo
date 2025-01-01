from src.registro.infrastructure.mongod import MongodRegistro
from ..application.response import RegistroResponse

class RegistroController:

    def __init__(self):
        self.mongo_number_validar = MongodRegistro()
        self.response = RegistroResponse()

    def registro(self, id, type):
        listaRegistro = self.mongo_number_validar.RegistroConnect(id, type)
        array = self.response.Registro(listaRegistro, type)
        return array





