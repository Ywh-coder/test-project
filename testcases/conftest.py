import pytest
from common.data_loader import load_data
from common.logger import get_logger
from common.request_util import RequestUtil

logger = get_logger(__name__)
BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def client():
    return RequestUtil(BASE_URL)


@pytest.fixture(scope="session")
def auth_token(client):
    payload = load_data()["login_creds"]
    resp = client.post("/auth", json=payload)
    assert resp.status_code == 200, f"登录失败: {resp.text}"
    return resp.json()["token"]


@pytest.fixture
def create_booking(client, auth_token):
    payload = load_data()["create_payload"]
    resp = client.post("/booking", json=payload)
    assert resp.status_code == 200
    booking_id = resp.json()["bookingid"]
    yield booking_id
    # teardown：用例可能已经删除了该 booking，405/404 视为已清理
    resp = client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )
    if resp.status_code not in (201, 404, 405):
        logger.warning(f"清理 booking {booking_id} 异常: {resp.status_code}")
