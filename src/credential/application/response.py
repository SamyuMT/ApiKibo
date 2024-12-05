class CredentialResponse():

    @staticmethod
    def parsedCredential(credential_info):
        if credential_info:
            return {
                "id": str(credential_info.get("_id")),
                "email":  credential_info.get("email"),
                "cel_number": credential_info.get("cel_mobile"),
                "state": True
            }
        else:
            raise Exception("Usuario o contraseña incorrectos")