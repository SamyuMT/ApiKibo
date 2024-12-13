def reestructurar_cadena(diccionario, id):
    transformed_data = {
        "id_user": id,
        "rol": diccionario.get("rol"),
        "nick_name": diccionario.get("nick_name"),
        "name": diccionario.get("name"),
        "last_name": diccionario.get("last_name"),
        "img_url": diccionario.get("img_url"),
    }
    return transformed_data

class CrearUserResponse():

    @staticmethod
    def SetCrearUser(col, data, id):
        if data:
            newData = reestructurar_cadena(data, id)
            result = col.insert_one(newData)
            print(result)

            return True
        else:
            return False       