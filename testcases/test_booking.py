class TestBooking:
    def test_get_booking_ids(self, client):
        resp = client.get("/booking")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
        assert len(resp.json()) > 0

    def test_create_booking(self, client):
        payload = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 150,
            "depositpaid": False,
            "bookingdates": {"checkin": "2025-02-01", "checkout": "2025-02-03"},
            "additionalneeds": "Lunch"
        }
        resp = client.post("/booking", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "bookingid" in data
        assert data["booking"]["firstname"] == "Test"

    def test_get_booking_detail(self, client, create_booking):
        resp = client.get(f"/booking/{create_booking}")
        assert resp.status_code == 200
        assert resp.json()["firstname"] == "Ywh"

    def test_update_booking(self, client, create_booking, auth_token):
        payload = {
            "firstname": "Updated",
            "lastname": "Name",
            "totalprice": 300,
            "depositpaid": True,
            "bookingdates": {"checkin": "2025-03-01", "checkout": "2025-03-05"},
            "additionalneeds": "Dinner"
        }
        headers = {"Cookie": f"token={auth_token}"}
        resp = client.put(f"/booking/{create_booking}", json=payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["firstname"] == "Updated"

    def test_delete_booking(self, client, create_booking, auth_token):
        headers = {"Cookie": f"token={auth_token}"}
        resp = client.delete(f"/booking/{create_booking}", headers=headers)
        assert resp.status_code == 201

    def test_get_nonexistent_booking(self, client):
        resp = client.get("/booking/99999999")
        assert resp.status_code == 404
