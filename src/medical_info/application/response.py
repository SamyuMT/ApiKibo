class MedicalInfoResponse():

    @staticmethod
    def parsedMedicalInfo(medical_info):
        if medical_info:
            return {
                "insurance": medical_info.get("insurance"),
                "type_link": medical_info.get("type_link"),
                "id_doctor": medical_info.get("id_doctor"),
                "state": True
            }
        else:
            raise Exception("informacion no encontrado")