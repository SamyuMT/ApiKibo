def reestructurar_cadena(diccionario, id):
    transformed_data = {
        "id_user": id,
        "gender": diccionario.get("gender"),
        "type_doc": diccionario.get("type_doc"),
        "doc_number": diccionario.get("doc_number"),
        "department": diccionario.get("department"),
        "city": diccionario.get("city"),
        "neighborhood": diccionario.get("neighborhood"),
        "type_street": diccionario.get("type_street"),
        "street_number": diccionario.get("street_number"),
        "house_number": diccionario.get("house_number"),
    }
    return transformed_data

class CrearUserInfoResponse():

    @staticmethod
    def SetCrearUserInfo(col, data, id):
        if data:
            newData = reestructurar_cadena(data, id)
            result = col.insert_one(newData)
            print(result)

            return True
        else:
            return False       