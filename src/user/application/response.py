class UserResponse():

    @staticmethod
    def parsedUser(user_info):
        if user_info:
            return {
                "rol": user_info.get("rol"),
                "nick_name": user_info.get("nick_name"),
                "name": user_info.get("name"),
                "last_name": user_info.get("last_name"),
                "img_url": user_info.get("img_url"),
                "state": True
            }
        else:
            raise Exception("Usuario no encontrado")