from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_doctors_schedule_returns_specialization():
    response = client.get("/doctors/schedule")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4
    first = data[0]
    assert "full_name" in first
    assert "reception_time" in first
    assert "specialization" in first


def test_auth_and_get_appointments_success():
    # data taken from exam ticket
    login_payload = {"phone_number": "+78986664502", "sms_code": "5500"}
    resp_login = client.post("/auth/login", json=login_payload)
    assert resp_login.status_code == 200
    token = resp_login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    resp_appts = client.get("/appointments", headers=headers)
    assert resp_appts.status_code == 200
    data = resp_appts.json()
    assert isinstance(data, list)
    # At least one appointment from seed data
    assert len(data) >= 1
    first = data[0]
    assert first["phone_number"] == "+78986664502"
    assert "doctor" in first
    assert "specialization" in first["doctor"]


def test_auth_fails_with_wrong_code():
    login_payload = {"phone_number": "+78986664502", "sms_code": "9999"}
    resp_login = client.post("/auth/login", json=login_payload)
    assert resp_login.status_code == 401

