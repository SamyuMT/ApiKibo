from src.info_user.infrastructure.mongod import MongodUserInfo
from ..application.response import UserInfoResponse

class UserInfoController:

    def __init__(self):
        self.mongo_user_info = MongodUserInfo()
        self.response = UserInfoResponse()

    def authenticate_user_info(self, id_user):
        user_info = self.mongo_user_info.UserInfoConnect(id_user)
        parsed = self.response.parsedUserInfo(user_info)
        return parsed


