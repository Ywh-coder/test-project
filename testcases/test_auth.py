import pytest
from common.data_loader import load_data


class TestAuth:
    @pytest.mark.smoke
    def test_login_success(self, client):
        payload = load_data()["login_creds"]
        resp = client.post("/auth", json=payload)
        assert resp.status_code == 200
        assert "token" in resp.json()

    @pytest.mark.regression
    def test_login_wrong_password(self, client):
        case = next(
            c for c in load_data()["login_invalid_cases"]
            if c["name"] == "wrong_password"
        )
        payload = {"username": case["username"], "password": case["password"]}
        resp = client.post("/auth", json=payload)
        assert resp.status_code == 200
        assert resp.json().get("reason") == case["expected_reason"]

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "case",
        [c for c in load_data()["login_invalid_cases"] if c["name"] != "wrong_password"],
        ids=lambda c: c["name"],
    )
    def test_login_empty_params(self, client, case):
        payload = {"username": case["username"], "password": case["password"]}
        resp = client.post("/auth", json=payload)
        assert resp.status_code == 200
        assert "token" not in resp.json()