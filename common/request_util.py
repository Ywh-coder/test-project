import requests
from common.logger import get_logger

logger = get_logger(__name__)


class RequestUtil:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        url = self.base_url + path
        logger.info(f"请求: {method} {url}, 参数: {kwargs}")
        resp = self.session.request(method, url, **kwargs)
        logger.info(f"响应: {resp.status_code}, {resp.text[:200]}")
        return resp

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)
