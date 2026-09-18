import pytest


class TestAuth:
    @pytest.mark.smoke
    def test_login_success(self, client):
        payload = {"username": "admin", "password": "password123"}
        resp = client.post("/auth", json=payload)
        assert resp.status_code == 200
        assert "token" in resp.json()

    @pytest.mark.regression
    def test_login_wrong_password(self, client):
        payload = {"username": "admin", "password": "wrong"}
        resp = client.post("/auth", json=payload)
        assert resp.status_code == 200
        assert resp.json().get("reason") == "Bad credentials"

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password", [
        ("", "password123"),
        ("admin", ""),
        ("", ""),
    ])
    def test_login_empty_params(self, client, username, password):
        resp = client.post("/auth", json={"username": username, "password": password})
        assert resp.status_code == 200
        assert "token" not in resp.json()
