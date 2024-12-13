from src.crear_doctor.infrastructure.mongod import MongodCrearDoctor
from ..application.response import CrearDoctorResponse

class CrearDoctorController:

    def __init__(self):
        self.mongo_number_validar = MongodCrearDoctor()
        self.response = CrearDoctorResponse()

    def crear_Doctor(self, data, id):
        col = self.mongo_number_validar.CrearDoctorConnect()
        parsed = self.response.SetCrearDoctor(col, data, id)
        return parsed


