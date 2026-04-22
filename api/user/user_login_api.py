from api.base_api import BaseUserApi


class UserLoginApi(BaseUserApi):
    def __init__(self, username, password):
        super().__init__()
        self.url = f"{self.host}/kejiyinhangyewuguanli/yonghu/login"
        self.method = "POST"
        self.data = {
            "username": username,
            "password": password
        }
