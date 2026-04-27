from common.client import RequestsClient
from common.file_load import load_yaml_file
from config.environment import ip_address
from paths_manager import http_yaml_path


# 普通用户类
class BaseUserApi(RequestsClient):
    # 类属性，这个是属于用户类的，不能跟其他角色token混用
    user_token = ""

    # BaseUserApi构造函数
    def __init__(self):
        # 在初始化BaseUserApi的时候先初始化父类的构造函数
        super().__init__()
        # 声明子类的属性
        self.host = ip_address
        # 插入我的请求头
        self.headers = {
            "Token": BaseUserApi.user_token
        }


# 审核人员类
class BaseReviewerApi(RequestsClient):
    # 类属性，这个是属于审核类的，不能跟其他角色token混用
    reviewer_token = ""

    # BaseReviewerApi构造函数
    def __init__(self):
        # 在初始化BaseReviewerApi的时候先初始化父类的构造函数
        super().__init__()
        # 声明子类的属性
        self.host = ip_address
        # 插入我的请求头
        self.headers = {
            "Token": BaseReviewerApi.reviewer_token
        }


# 业务人员类
class BaseBusinessApi(RequestsClient):
    # 类属性，这个是属于业务类的，不能跟其他角色token混用
    business_token = ""

    # BaseBusinessApi构造函数
    def __init__(self):
        # 在初始化BaseBusinessApi的时候先初始化父类的构造函数
        super().__init__()
        # 声明子类的属性
        self.host = load_yaml_file(http_yaml_path)['basic']
        # 插入我的请求头
        self.headers = {
            "Token": BaseBusinessApi.business_token
        }


# 管理员类
class BaseAdminApi(RequestsClient):
    # 类属性，这个是属于管理员类的，不能跟其他角色token混用
    admin_token = ""

    # BaseAdminApi构造函数
    def __init__(self):
        # 在初始化BaseAdminApi的时候先初始化父类的构造函数
        super().__init__()
        # 声明子类的属性
        self.host = load_yaml_file(http_yaml_path)['basic']
        # 插入我的请求头
        self.headers = {
            "Token": BaseAdminApi.admin_token
        }
