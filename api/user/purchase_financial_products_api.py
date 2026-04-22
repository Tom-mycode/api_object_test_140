from api.base_api import BaseUserApi


class PurchaseFinancialProductsApi(BaseUserApi):
    def __init__(self, licaicanpinId, licaicanpinGoumaiUuidNumber, licaicanpinGoumaiFenshu):
        super().__init__()
        self.url = f"{self.host}/kejiyinhangyewuguanli/licaicanpinGoumai/save"
        self.method = "post"
        self.json = {
            "licaicanpinId": licaicanpinId,
            "licaicanpinGoumaiUuidNumber": licaicanpinGoumaiUuidNumber,
            "licaicanpinGoumaiFenshu": licaicanpinGoumaiFenshu
        }