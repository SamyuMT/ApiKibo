from ..application.response import PrediccionResponse

class PrediccionController:

    def __init__(self):
        self.response = PrediccionResponse()

    def prediccion(self, data):
        parsed = self.response.SetPrediccion(data)
        return parsed


