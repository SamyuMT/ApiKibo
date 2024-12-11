from src.validar_email.infrastructure.mongod import MongodValidarEmail
from ..application.response import ValidarEmailResponse

class ValidarEmailController:

    def __init__(self):
        self.mongo_email_validar = MongodValidarEmail()
        self.response = ValidarEmailResponse()

    def authenticate_validar_email(self, email):
        info = self.mongo_email_validar.ValidarEmailConnect(email)
        parsed = self.response.parsedValidarEmail(info)
        return parsed


