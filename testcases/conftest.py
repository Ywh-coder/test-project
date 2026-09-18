import os
import pytest
from common.data_loader import load_data
from common.logger import get_logger
from common.request_util import RequestUtil

logger = get_logger(__name__)
BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")


def pytest_configure(config):
    """pytest 启动时确保 report 目录存在，避免 --html 写文件失败"""
    os.makedirs("report", exist_ok=True)


@pytest.fixture(scope="session")
def client():
    c = RequestUtil(BASE_URL)
    yield c
    c.close()


@pytest.fixture(scope="session")
def auth_token(client):
    payload = load_data()["login_creds"]
    resp = client.post("/auth", json=payload)
    assert resp.status_code == 200, f"登录失败: {resp.text}"
    return resp.json()["token"]


@pytest.fixture
def create_booking(client, auth_token):
    """
    创建 booking，用例结束后自动清理。
    用例可能已主动删除，405/404 视为已清理，只有非预期状态才打 warning。
    """
    payload = load_data()["create_payload"]
    resp = client.post("/booking", json=payload)
    assert resp.status_code == 200
    booking_id = resp.json()["bookingid"]

    yield booking_id

    resp = client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )
    if resp.status_code not in (201, 404, 405):
        logger.warning(f"清理 booking {booking_id} 异常: {resp.status_code}")
@pytest.fixture
def booking_cleaner(client, auth_token):
    """
    收集用例中创建的 booking_id，用例结束后统一清理。
    用法：
        def test_xxx(client, booking_cleaner):
            resp = client.post("/booking", json=payload)
            bid = resp.json()["bookingid"]
            booking_cleaner.append(bid)
    """

    ids = []
    yield ids
    for bid in ids:
        resp = client.delete(
            f"/booking/{bid}",
            headers={"Cookie": f"token={auth_token}"}
        )
        # RESTful Booker 对不存在的 booking_id 删除返回 405（Method Not Allowed），非 404
        #DELETE 一个不存在的资源应该返回 404，表示资源未找到。但很多框架在找不到匹配的路由处理函数时，会统一返回 405。
        if resp.status_code not in (201, 404, 405):
            logger.warning(f"清理 booking {bid} 异常: {resp.status_code}")