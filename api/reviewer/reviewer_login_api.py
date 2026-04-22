from api.base_api import BaseReviewerApi


class ReviewerLoginApi(BaseReviewerApi):
    def __init__(self, username, password):
        super().__init__()
        self.url = f"{self.host}/kejiyinhangyewuguanli/shenherenyuan/login"
        self.method = "POST"
        self.data = {
            "username": username,
            "password": password
        }