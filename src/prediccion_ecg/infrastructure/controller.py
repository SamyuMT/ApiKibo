from ..application.response import PrediccionResponse

class PrediccionController:

    def __init__(self):
        self.response = PrediccionResponse()

    def prediccion(self, data, model):
        parsed = self.response.SetPrediccion(data, model)
        return parsed


