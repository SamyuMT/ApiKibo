from src.listar_registros.infrastructure.mongod import MongodListarRegistros
from ..application.response import ListarRegistrosResponse

class ListarRegistrosController:

    def __init__(self):
        self.mongoRegistros = MongodListarRegistros()
        self.response = ListarRegistrosResponse()

    def listarRegistros(self):
        listaRegistro = self.mongoRegistros.ListarRegistrosConnect()
        lista = self.response.ListarRegistros(listaRegistro)
        return lista





