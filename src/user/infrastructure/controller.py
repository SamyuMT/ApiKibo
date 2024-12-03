from src.user.infrastructure.mongod import MongodUser
from ..application.response import UserResponse

class UserController:

    def __init__(self):
        self.mongo_user = MongodUser()
        self.response = UserResponse()

    def authenticate_user(self, credential, pasw):
        user_info = self.mongo_user.UserConnect(credential, pasw)
        parsed = self.response.parsedUser(user_info)
        return parsed


