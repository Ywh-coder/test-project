import pytest
from common.data_loader import load_data


class TestBooking:
    @pytest.mark.smoke
    def test_get_booking_ids(self, client):
        resp = client.get("/booking")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
        assert len(resp.json()) > 0

    @pytest.mark.smoke
    @pytest.mark.parametrize("variant", load_data()["create_payload_variants"])
    def test_create_booking(self, client, variant):
        resp = client.post("/booking", json=variant["payload"])
        assert resp.status_code == 200
        data = resp.json()
        assert "bookingid" in data
        assert data["booking"]["firstname"] == variant["payload"]["firstname"]

    @pytest.mark.regression
    def test_get_booking_detail(self, client, create_booking):
        resp = client.get(f"/booking/{create_booking}")
        assert resp.status_code == 200
        expected = load_data()["create_payload"]["firstname"]
        assert resp.json()["firstname"] == expected

    @pytest.mark.regression
    def test_update_booking(self, client, create_booking, auth_token):
        payload = load_data()["update_payload"]
        headers = {"Cookie": f"token={auth_token}"}
        resp = client.put(f"/booking/{create_booking}", json=payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["firstname"] == "Updated"

    @pytest.mark.regression
    def test_delete_booking(self, client, create_booking, auth_token):
        headers = {"Cookie": f"token={auth_token}"}
        resp = client.delete(f"/booking/{create_booking}", headers=headers)
        assert resp.status_code == 201

    @pytest.mark.regression
    def test_get_nonexistent_booking(self, client):
        resp = client.get("/booking/99999999")
        assert resp.status_code == 404
