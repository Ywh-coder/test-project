import pytest
from common.request_util import RequestUtil

BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def client():
    return RequestUtil(BASE_URL)


@pytest.fixture(scope="session")
def auth_token(client):
    payload = {"username": "admin", "password": "password123"}
    resp = client.post("/auth", json=payload)
    assert resp.status_code == 200, f"登录失败: {resp.text}"
    token = resp.json()["token"]
    return token


@pytest.fixture
def create_booking(client):
    payload = {
        "firstname": "Ywh",
        "lastname": "Coder",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-01-01", "checkout": "2025-01-05"},
        "additionalneeds": "Breakfast"
    }
    resp = client.post("/booking", json=payload)
    assert resp.status_code == 200
    booking_id = resp.json()["bookingid"]
    yield booking_id
    # 测试结束后清理数据
    client.delete(f"/booking/{booking_id}", headers={"Cookie": f"token={auth_token}"})
