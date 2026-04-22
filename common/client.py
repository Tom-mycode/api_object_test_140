import requests

from common.logger import GetLogger


class RequestsClient:
    # 类属性
    session = requests.session()

    # 定义这个类的属性
    def __init__(self):
        self.url = None
        self.method = None
        self.headers = None
        self.params = None
        self.data = None
        self.json = None
        self.files = None
        self.resp = None

    # 定义了请求函数，因为我们要在里面添加请求的内容以及异常捕获，方便第二天上班的时候调试代码
    def send(self):
        logger = GetLogger.get_logger()

        logger.debug('==================== 接口请求开始 ====================')
        logger.debug(f'接口 url: {self.url}')
        logger.debug(f'接口 method: {self.method}')
        logger.debug(f'接口 headers: {self.headers}')
        logger.debug(f'接口 params: {self.params}')
        logger.debug(f'接口 data: {self.data}')
        logger.debug(f'接口 json: {self.json}')
        logger.debug(f'接口 files: {self.files}')

        # 异常捕获你要发送的接口参数
        try:
            self.resp = RequestsClient.session.request(
                url=self.url,
                method=self.method,
                headers=self.headers,
                params=self.params,
                data=self.data,
                json=self.json,
                files=self.files,
                verify=False  # 不校验https证书，加了可以请求https，忽略安全警告
            )
            # 发送完成后的返回值和状态码
            logger.debug(f"接口响应状态码：{self.resp.status_code}")
            logger.debug(f"接口响应body:{self.resp.text}")
            logger.debug("==============接口请求结束================")
            self.resp.raise_for_status()
        except requests.exceptions.RequestException:
            logger.error(f"接口请求异常，url={self.url},method={self.method}", exc_info=True)
            raise
        return self.resp


if __name__ == '__main__':
    client = RequestsClient()
    client.method = "POST"  # 请求方法
    client.url = "https://httpbin.org/post"  # 接口地址
    client.headers = {"User-Agent": "TestClient"}  # 请求头
    client.json = {"username": "admin", "password": "123456"}  # JSON 请求体
    resp = client.send()
    print(resp.status_code)
    print(resp.json())
