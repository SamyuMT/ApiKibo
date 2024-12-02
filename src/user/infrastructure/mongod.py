from ...mongo.connect import ConnectionMongo

class MongodUser:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def UserConnect(self, creditial, pasw):
        print(creditial,pasw)
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["users"]
        # Verificar si creditial es un email o un número de teléfono
        if "@" in creditial:  # Es un correo electrónico
            user = col.find_one({"email": creditial, "password": pasw}, {"_id": False})
        else:  # Se asume que es un número de teléfono
            user = col.find_one({"cel_number": creditial, "password": pasw}, {"_id": False})

        return user
