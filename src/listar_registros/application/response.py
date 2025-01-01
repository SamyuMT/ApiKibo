def reestructurar_cadena(registro):
    transformed_data = {
        "_id": registro.get("_id"),
        "id_user": registro.get("id_user"),
        "full_name": registro.get("full_name"),
        "email": registro.get("email"),
        "created_date": registro.get("created_date"),
        "created_time": registro.get("created_time"),
        "type": registro.get("type"),
        "length": registro.get("length"),
    }
    return transformed_data

class ListarRegistrosResponse():

    @staticmethod
    def ListarRegistros(listaRegistro):
        parsed_registros = []
        for registro in listaRegistro:
            parsed = reestructurar_cadena(registro)
            parsed_registros.append(parsed)
        return parsed_registros
