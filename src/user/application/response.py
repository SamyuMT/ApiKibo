class UserResponse():

    @staticmethod
    def parsedUser(user_info):
        if user_info:
            return {
                "cel_number": user_info.get("cel_number"),
                "name": user_info.get("name"),
                "rol": user_info.get("rol")
            }
        else:
            raise Exception("Usuario o contraseña incorrectos")