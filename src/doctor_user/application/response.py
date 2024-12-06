class DoctorResponse():

    @staticmethod
    def parsedDoctor(doctor_info):
        if doctor_info:
            return {
                "name": doctor_info.get("name"),
                "last_name": doctor_info.get("last_name"),
                "specialty": doctor_info.get("specialty"),
                "institution": doctor_info.get("institution"),
                "email": doctor_info.get("email"),
                "state": True
            }
        else:
            raise Exception("Doctor no encontrado")