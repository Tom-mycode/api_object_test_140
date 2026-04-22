import uuid

import allure
from jsonpath import jsonpath

from api.reviewer.review_financial_products_api import ListReviewerFinancialProductsApi, ReviewFinancialProductsApi
from api.user.purchase_financial_products_api import PurchaseFinancialProductsApi


@allure.epic("主流程测试")
@allure.feature("理财产品购买流程测试")
class TestPurchaseFlow:
    uuid_str = ""

    fp_id = ""

    # 购买理财产品
    @allure.title("购买理财产品接口")
    def test_purchase_fp_api(self, db_init, fp_stock_init):
        TestPurchaseFlow.uuid_str = str(uuid.uuid1())
        resp = PurchaseFinancialProductsApi(
            licaicanpinId=3,
            licaicanpinGoumaiUuidNumber=TestPurchaseFlow.uuid_str,
            licaicanpinGoumaiFenshu=2).send()
        db_res = db_init.query(
            f"""
                   SELECT *
                   FROM `licaicanpin_goumai`
                   WHERE `licaicanpin_goumai_uuid_number` = '{TestPurchaseFlow.uuid_str}'
                   """)
        assert resp.status_code == 200
        # 该记录存在
        assert db_res
        # 个数为1
        assert len(db_res) == 1
        # 查出的最新的记录的uuid和传入的一致
        assert db_res[0]['licaicanpin_goumai_uuid_number'] == TestPurchaseFlow.uuid_str

    # 展示待审核列表
    @allure.title("调用审核列表接口")
    def test_list_reviewer_financial_products_api(self, db_init):
        resp = ListReviewerFinancialProductsApi().send()
        TestPurchaseFlow.fp_id = jsonpath(resp.json(), "$..data.list[0].id")[0]
        assert resp.status_code == 200
        assert resp.json()["code"] == 0

        # 断言这个id是不是存在
        assert TestPurchaseFlow.fp_id

        # 检测这个id在数据库是不是也存在
        db_res = db_init.query(
            f"""
                       SELECT *
                       FROM `licaicanpin_goumai`
                       WHERE `id` = {TestPurchaseFlow.fp_id}
                   """
        )
        assert db_res

    # 审核理财产品
    @allure.title("审核理财产品接口")
    def test_review_financial_products_api(self, db_init):
        resp = ReviewFinancialProductsApi(
            TestPurchaseFlow.fp_id,
            2,
            "agree").send()
        assert resp.status_code == 200
        assert resp.json().get("code") == 0
        # 断言审核的结果是不是同意
        db_res = db_init.query(
            f"""
                   SELECT `licaicanpin_goumai_yesno_types`
                   FROM `licaicanpin_goumai`
                   WHERE `id` = {TestPurchaseFlow.fp_id}
                   """
        )
        assert db_res
        actual_status = db_res[0]["licaicanpin_goumai_yesno_types"]
        assert actual_status == 2
