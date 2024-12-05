from src.doctor_user.infrastructure.mongod import MongodDoctor
from ..application.response import DoctorResponse

class DoctorController:

    def __init__(self):
        self.mongo_doctor = MongodDoctor()
        self.response = DoctorResponse()

    def authenticate_doctor(self, id_doctor):
        doctor_info = self.mongo_doctor.DoctorConnect(id_doctor)
        parsed = self.response.parsedDoctor(doctor_info)
        return parsed


