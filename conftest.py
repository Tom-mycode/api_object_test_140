from typing import List
import pytest

from api.base_api import BaseUserApi, BaseReviewerApi
from api.reviewer.reviewer_login_api import ReviewerLoginApi
from api.user.user_login_api import UserLoginApi
from common.db_util import DBUtil
from common.file_load import load_yaml_file
from common.logger import GetLogger
from config.environment import db_host
from paths_manager import db_yaml_path


def pytest_collection_modifyitems(items: List["item"]):
    for item in items:
        item._nodeid = item._nodeid.encode('utf-8').decode("unicode-escape")


@pytest.fixture(scope='session', autouse=True)
def logger_init():
    GetLogger.get_logger().info("日志初始化成功")


@pytest.fixture(scope="session", autouse=True)
def user_login():
    user_login_api = UserLoginApi(username="user1", password="123456")
    resp = user_login_api.send()
    # 获取token
    BaseUserApi.user_token = resp.json()["token"]


@pytest.fixture(scope="session", autouse=True)
def reviewer_login():
    reviewer_login_api = ReviewerLoginApi(username="shenhe1", password="123456")
    resp = reviewer_login_api.send()
    # 获取token
    BaseReviewerApi.reviewer_token = resp.json()["token"]


@pytest.fixture(scope="session", autouse=False)
def db_init():
    db_info = load_yaml_file(db_yaml_path)
    db_util = DBUtil(
        host=db_info["host"],
        user=db_info["username"],
        password=db_info["password"])
    yield db_util


@pytest.fixture(scope='session', autouse=False)
def fp_stock_init(db_init, fp_id=3, user_id=3):
    db_init.execute(
        f"""
        UPDATE `licaicanpin` SET `licaicanpin_fenshu` = 1000 where id = {fp_id}
        """
    )
    yield
    db_init.execute(
        f"""
        UPDATE `yinhangka` SET `yinghangka_money` = 10000000 where id = {user_id}
        """
    )
