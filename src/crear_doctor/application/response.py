def reestructurar_cadena(diccionario, id):
    transformed_data = {
        "name": diccionario.get("name"),
        "last_name": diccionario.get("last_name"),
        "specialty": diccionario.get("specialty"),
        "institution": diccionario.get("institution"),
        "email": diccionario.get("email"),
    }
    return transformed_data

class CrearDoctorResponse():

    @staticmethod
    def SetCrearDoctor(col, data, id):
        if data:
            newData = reestructurar_cadena(data, id)
            result = col.insert_one(newData)
            print(result)

            return True
        else:
            return False       