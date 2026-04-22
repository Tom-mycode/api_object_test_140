"""
定义项目的根路径
解决痛点：项目移植后无法使用
"""
import os

# 获取当前文件的绝对路径，在取其根目录
project_path = os.path.dirname(os.path.abspath(__file__))

# 编写yaml文件的路径
# join = /
bank_system_data_yaml = os.path.join(
    project_path, 'data', 'bank_system_data.yaml'
)

# http公共配置文件
http_yaml_path = os.path.join(
    project_path, 'config', 'http.yaml'
)

# db公共配置文件
db_yaml_path = os.path.join(
    project_path, 'config', 'db.yaml'
)

if __name__ == '__main__':
    print(project_path)
    print(bank_system_data_yaml)
    print(http_yaml_path)
    print(db_yaml_path)
