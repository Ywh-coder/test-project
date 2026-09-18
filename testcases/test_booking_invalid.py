import pytest
from common.data_loader import load_data


def _invalid_cases():
    return load_data()["invalid_payloads"]


class TestBookingInvalid:
    """预订接口异常用例"""

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "case",
        [
            pytest.param(
                c,
                marks=pytest.mark.xfail(
                    reason=c.get("reason", "已知 API 缺陷"),
                    strict=True,
                )
                if c.get("xfail")
                else [],
                id=c["name"],
            )
            for c in _invalid_cases()
        ],
    )
    def test_create_booking_invalid_fields(self, client, case, booking_cleaner):
        resp = client.post("/booking", json=case["payload"])
        assert resp.status_code == case["expected_status"]
        if resp.status_code == 200 and "bookingid" in resp.json():
            booking_cleaner.append(resp.json()["bookingid"])

    @pytest.mark.regression
    def test_update_without_auth_token(self, client, create_booking):
        payload = load_data()["update_payload"]
        resp = client.put(f"/booking/{create_booking}", json=payload)
        assert resp.status_code == 403

    @pytest.mark.regression
    def test_delete_nonexistent_booking(self, client, auth_token):
        headers = {"Cookie": f"token={auth_token}"}
        resp = client.delete("/booking/99999999", headers=headers)
        assert resp.status_code in (404, 405)