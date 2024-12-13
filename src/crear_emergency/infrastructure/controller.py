from src.crear_emergency.infrastructure.mongod import MongodCrearEmergencyInfo
from ..application.response import CrearEmergencyInfoResponse

class CrearEmergencyInfoController:

    def __init__(self):
        self.mongo_number_validar = MongodCrearEmergencyInfo()
        self.response = CrearEmergencyInfoResponse()

    def crear_EmergencyInfo(self, data, id):
        col = self.mongo_number_validar.CrearEmergencyInfoConnect()
        parsed = self.response.SetCrearEmergencyInfo(col, data, id)
        return parsed


