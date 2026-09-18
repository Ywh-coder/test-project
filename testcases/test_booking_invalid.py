import pytest
from common.data_loader import load_data


class TestBookingInvalid:
    """预订接口异常用例"""

    @pytest.mark.regression
    @pytest.mark.parametrize("case", load_data()["invalid_payloads"])
    def test_create_booking_invalid_fields(self, client, case):
        resp = client.post("/booking", json=case["payload"])
        assert resp.status_code == case["expected_status"]

    @pytest.mark.regression
    def test_update_without_auth_token(self, client, create_booking):
        payload = load_data()["update_payload"]
        resp = client.put(f"/booking/{create_booking}", json=payload)
        assert resp.status_code == 403

    @pytest.mark.regression
    def test_delete_nonexistent_booking(self, client, auth_token):
        headers = {"Cookie": f"token={auth_token}"}
        resp = client.delete("/booking/99999999", headers=headers)
        # RESTful Booker 对不存在的 booking_id 返回 405 Method Not Allowed
        assert resp.status_code in (404, 405)
