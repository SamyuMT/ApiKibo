def reestructurar_cadena(diccionario):
    transformed_data = {
        'email': diccionario.get('email', ''),  # Si no hay 'email', se usa ''
        'cel_mobile': diccionario.get('cel_number', ''),  # Renombrar 'cel_number' a 'cel_mobile'
        'pass': diccionario.get('id', '')  # Renombrar 'id' a 'pass'
    }
    return transformed_data

class CrearCredentialResponse():

    @staticmethod
    def SetCrearCredential(col, data):
        if data:
            newData = reestructurar_cadena(data)
            result = col.insert_one(newData)
            print(result)

            return True
        else:
            return False            