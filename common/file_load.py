import yaml

from paths_manager import bank_system_data_yaml


def load_yaml_file(file_path):
    # 打开我们的yaml文件
    with open(file_path, 'r', encoding='utf-8') as f:
        # 将yaml文件返回为字典格式
        return yaml.safe_load(f)


if __name__ == '__main__':
    print(load_yaml_file(bank_system_data_yaml))
