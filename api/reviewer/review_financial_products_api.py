from api.base_api import BaseReviewerApi


class ListReviewerFinancialProductsApi(BaseReviewerApi):
    def __init__(self):
        super().__init__()
        self.url = f"{self.host}/kejiyinhangyewuguanli/licaicanpinGoumai/page"
        self.method = "get"
        self.params = {
            "page": 1,
            "limit": 10,
            "licaicanpinGoumaiDelete": 1
        }


class ReviewFinancialProductsApi(BaseReviewerApi):
    def __init__(self, id, licaicanpinGoumaiYesnoTypes, licaicanpinGoumaiYesnoText):
        super().__init__()
        self.url = f"{self.host}/kejiyinhangyewuguanli/licaicanpinGoumai/shenhe"
        self.method = "post"
        self.json = {
            "id": id,
            "licaicanpinGoumaiYesnoTypes": licaicanpinGoumaiYesnoTypes,
            "licaicanpinGoumaiYesnoText": licaicanpinGoumaiYesnoText
        }
