from src.emergency_user.infrastructure.mongod import MongodUserEmergency
from ..application.response import UserEmergencyResponse

class UserEmergencyController:

    def __init__(self):
        self.mongo_user_emergency = MongodUserEmergency()
        self.response = UserEmergencyResponse()

    def authenticate_user_emergency(self, id_user):
        user_info = self.mongo_user_emergency.UserEmergencyConnect(id_user)
        parsed = self.response.parsedUserEmergency(user_info)
        return parsed


