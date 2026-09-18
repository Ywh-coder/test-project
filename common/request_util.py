import requests
from common.logger import get_logger

logger = get_logger(__name__)

# 敏感字段，日志里做脱敏
SENSITIVE_KEYS = {"token", "cookie", "authorization"}


def _mask(kwargs):
    """对请求参数中的敏感信息脱敏"""
    safe = {}
    for k, v in kwargs.items():
        if k.lower() == "headers" and isinstance(v, dict):
            safe[k] = {
                hk: ("***" if any(s in hk.lower() for s in SENSITIVE_KEYS) else hv)
                for hk, hv in v.items()
            }
        elif k.lower() == "json" and isinstance(v, dict):
            safe[k] = {
                jk: ("***" if any(s in jk.lower() for s in SENSITIVE_KEYS) else jv)
                for jk, jv in v.items()
            }
        else:
            safe[k] = v
    return safe


class RequestUtil:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method, path, timeout=None, **kwargs):
        url = self.base_url + path
        logger.info(f"请求: {method} {url}, 参数: {str(_mask(kwargs))[:300]}")
        resp = self.session.request(
            method, url, timeout=timeout or self.timeout, **kwargs
        )
        body = resp.text[:300] if resp.text else ""
        logger.info(f"响应: {resp.status_code}, body: {body}")
        return resp

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)

    def close(self):
        self.session.close()