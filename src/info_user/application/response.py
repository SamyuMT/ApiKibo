class UserInfoResponse():

    @staticmethod
    def parsedUserInfo(user_info):
        if user_info:
            return {
                "gender": user_info.get("gender"),
                "type_doc": user_info.get("type_doc"),
                "doc_number": user_info.get("doc_number"),
                "department": user_info.get("department"),
                "city": user_info.get("city"),
                "neighborhood": user_info.get("neighborhood"),
                "type_street": user_info.get("type_street"),
                "street_number": user_info.get("street_number"),
                "house_number": user_info.get("house_number"),
                "state": True
            }
        else:
            raise Exception("Usuario no encontrado")