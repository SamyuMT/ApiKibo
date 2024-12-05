from ...mongo.connect import ConnectionMongo

class MongodCredential:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def CredentialConnect(self, credential, pasw):
        print(credential,pasw)
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["credential"]
        # Verificar si creditial es un email o un número de teléfono
        if "@" in credential:  # Es un correo electrónico
            user = col.find_one({"email": credential, "pass": pasw})
        else:  # Se asume que es un número de teléfono
            user = col.find_one({"cel_mobile": credential, "pass": pasw})

        return user
