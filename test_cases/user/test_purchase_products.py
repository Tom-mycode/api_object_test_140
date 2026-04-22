import uuid

import allure
import pytest

from api.user.purchase_financial_products_api import PurchaseFinancialProductsApi
from common.file_load import load_yaml_file
from paths_manager import bank_system_data_yaml


@allure.epic("理财产品接口全覆盖")
@allure.feature("购买理财产品接口")
class TestPurchaseFinancialProducts:
    test_data = load_yaml_file(bank_system_data_yaml)['新增理财产品接口']

    @allure.title("购买理财产品接口用例")
    @pytest.mark.parametrize('case_name,product_id,num,expect_status,expect_body', test_data)
    def test_purchase_financial_products(self, case_name, product_id, num, expect_status, expect_body):
        purchase_financial_products = PurchaseFinancialProductsApi(
            licaicanpinId=product_id,
            licaicanpinGoumaiUuidNumber=str(uuid.uuid1()),
            licaicanpinGoumaiFenshu=num
        )
        resp = purchase_financial_products.send()
        pytest.assume(resp.status_code == expect_status)
        pytest.assume(resp.text == expect_body)
