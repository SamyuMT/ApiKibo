from ...mongo.connect import ConnectionMongo

class MongodUser:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def UserConnect(self, credential, pasw):
        print(credential,pasw)
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["users"]
        # Verificar si creditial es un email o un número de teléfono
        if "@" in credential:  # Es un correo electrónico
            user = col.find_one({"email": credential, "password": pasw})
        else:  # Se asume que es un número de teléfono
            user = col.find_one({"cel_number": credential, "password": pasw})

        return user
