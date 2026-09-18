import pytest
from common.data_loader import load_data
from common.request_util import RequestUtil

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
    # 测试结束后清理数据
    client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )
