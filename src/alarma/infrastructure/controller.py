from ..application.response import AlarmaResponse

class AlarmaController:

    def __init__(self):
        self.response = AlarmaResponse()

    def alarma(self, mensage, latitud, longitud, cel_emergencia, cel_contacto):
        parsed = self.response.SetAlarma(mensage, latitud, longitud, cel_emergencia, cel_contacto)
        return parsed


