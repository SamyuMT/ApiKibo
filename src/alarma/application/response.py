
import time
from twilio.rest import Client

class AlarmaResponse():

    ultimo_envio = 0
    
    @staticmethod
    def SetAlarma(mensage, latitud, longitud, cel_emergencia, cel_contacto):
        sec = time.time()
        if mensage and sec - AlarmaResponse.ultimo_envio >= 300:  # Verificar si pasaron 60 segundos
            # Crear la URL de Google Maps
            direccion_url = f"https://www.google.com/maps?q={latitud},{longitud}"
            # Agregar emojis al mensaje
            mensaje_alarma = f"🚨 ¡Alarma activada! {mensage} 🆘\n\nUbicación: {direccion_url}"
            # Enviar el mensaje a los dos números
            AlarmaResponse.enviar_whatsapp(mensaje_alarma, cel_emergencia)
            AlarmaResponse.enviar_whatsapp(mensaje_alarma, cel_contacto)
            # Actualizar el tiempo del último envío
            AlarmaResponse.ultimo_envio = sec
            return 1
        else:
            print("No han pasado 300 segundos desde el último envío.")
            return 0  


    @staticmethod
    def agregar_codigo_pais(numero):
        # Agregar el código de país +57 (Colombia) si no está presente
        numero = 'whatsapp:+57' + str(numero)
        return numero

    @staticmethod
    def enviar_whatsapp(mensaje, numero):
        # Configuración de credenciales de Twilio
        account_sid = 'AC90978f42d41789f5aee147d406d8dde4'
        auth_token = 'e85675de49f7c1e91c505b1388e28218'
        client = Client(account_sid, auth_token)
        num = AlarmaResponse.agregar_codigo_pais(numero)
        # Enviar el mensaje
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Número de WhatsApp de Twilio
            body=mensaje,  # Contenido del mensaje
            to=num  # Número de destino en formato internacional
        )

        # Imprimir SID del mensaje enviado
        print("Mensaje enviado con SID:", message.sid)
        