from src.medical_info.infrastructure.mongod import MongodMedicalInfo
from ..application.response import MedicalInfoResponse

class MedicalInfoController:

    def __init__(self):
        self.mongo_medical_info = MongodMedicalInfo()
        self.response = MedicalInfoResponse()

    def authenticate_medical_info(self, id_user):
        medical_info = self.mongo_medical_info.MedicalInfoConnect(id_user)
        parsed = self.response.parsedMedicalInfo(medical_info)
        return parsed


