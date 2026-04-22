import pymysql  # 导入 PyMySQL，用于连接 MySQL 数据库
from contextlib import contextmanager  # 导入 contextmanager，允许自定义上下文管理器（with 使用）
from pprint import pprint  # 美观打印 Python 数据结构

from common.file_load import load_yaml_file
from config.environment import db_host
from paths_manager import db_yaml_path


class DBUtil:
    def __init__(self, host, user, password, database="kejiyinhangyewuguanli", port=3306):
        """
        初始化数据库配置，仅保存连接参数，不立即连接数据库
        :param host: MySQL 地址
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名，默认 kejiyinhangyewuguanli
        :param port: 端口号，默认 3306
        """
        self.config = {
            "host": host,  # MySQL 主机地址
            "user": user,  # MySQL 用户名
            "password": password,  # MySQL 密码
            "port": port,  # 端口号
            "database": database,  # 使用的数据库
            "charset": "utf8mb4",  # 字符集，支持中文和 emoji
            "cursorclass": pymysql.cursors.DictCursor,  # 查询结果使用字典格式，而不是元组
        }

    @contextmanager
    def get_cursor(self):
        """
        自定义上下文管理器，用于管理数据库连接和游标（with 自动开启/关闭）
        逻辑：
        1. 创建连接
        2. 创建游标
        3. 让外部执行 SQL
        4. 自动提交/回滚
        5. 自动关闭游标和连接
        """
        conn = pymysql.connect(**self.config)  # 建立数据库连接
        cursor = conn.cursor()  # 创建游标对象，用于执行 SQL
        try:
            yield cursor  # 将游标“交给” with 代码块使用
            conn.commit()  # 如果 with 内没有异常，则提交事务
        except Exception as e:
            conn.rollback()  # 有异常则回滚，避免脏数据
            raise e  # 抛出异常，让调用者知道问题
        finally:
            cursor.close()  # 关闭游标
            conn.close()  # 关闭数据库连接

    def query(self, sql):
        """
        执行 SELECT 查询语句
        :param sql: 要执行的 SQL
        :return: 返回所有查询结果（列表，每条记录是字典）
        """
        with self.get_cursor() as cursor:  # 使用 with 语法自动管理连接和游标
            cursor.execute(sql)  # 执行 SQL 语句
            return cursor.fetchall()  # 返回所有查询结果

    def execute(self, sql):
        """
        执行写操作（INSERT、UPDATE、DELETE）
        :param sql: 修改类 SQL
        """
        with self.get_cursor() as cursor:  # with 结构保证自动提交/关闭
            cursor.execute(sql)  # 执行 SQL，不返回结果（增删改）


if __name__ == '__main__':
    # 创建数据库工具对象，填入连接信息
    db_info = load_yaml_file(db_yaml_path)
    db = DBUtil(host=db_info["host"], user=db_info["username"], password=db_info["password"])

    # SQL 查询语句，查询某个 uuid 的购买记录
    sql = '''
    SELECT * FROM licaicanpin_goumai
    '''

    # 执行查询
    result = db.query(sql)

    # 美观打印结果
    pprint(result)
