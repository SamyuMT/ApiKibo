from src.validar_number.infrastructure.mongod import MongodValidarNumber
from ..application.response import ValidarNumberResponse

class ValidarNumberController:

    def __init__(self):
        self.mongo_number_validar = MongodValidarNumber()
        self.response = ValidarNumberResponse()

    def authenticate_validar_number(self, number):
        info = self.mongo_number_validar.ValidarNumberConnect(number)
        parsed = self.response.parsedValidarNumber(info)
        return parsed


