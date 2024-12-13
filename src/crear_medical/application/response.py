def reestructurar_cadena(diccionario, id):
    transformed_data = {
        "id_user": id,
        "type_link": diccionario.get("type_link"),
        "id_doctor": diccionario.get("id_doctor"),
        "insurance": diccionario.get("insurance"),
    }
    return transformed_data

class CrearMedicalResponse():

    @staticmethod
    def SetCrearMedical(col, data, id):
        if data:
            newData = reestructurar_cadena(data, id)
            result = col.insert_one(newData)
            print(result)

            return True
        else:
            return False       