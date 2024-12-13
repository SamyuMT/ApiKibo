from src.crear_medical.infrastructure.mongod import MongodCrearMedical
from ..application.response import CrearMedicalResponse

class CrearMedicalController:

    def __init__(self):
        self.mongo_number_validar = MongodCrearMedical()
        self.response = CrearMedicalResponse()

    def crear_medical(self, data, id):
        col = self.mongo_number_validar.CrearMedicalConnect()
        parsed = self.response.SetCrearMedical(col, data, id)
        return parsed


