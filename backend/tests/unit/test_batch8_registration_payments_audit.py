import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.hackathon import Hackathon
from app.models.user import User
from app.models.registration import Registration
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, RegistrationStatus, PaymentStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_b8_fixtures():
    db = SessionLocal()

    hack = db.query(Hackathon).filter(Hackathon.id == "hack_b8_test").first()
    if not hack:
        hack = Hackathon(id="hack_b8_test", name="Batch 8 Registration Hackathon", status=HackathonStatus.ACTIVE)
        db.add(hack)

    user = db.query(User).filter(User.id == "usr_b8_participant").first()
    if not user:
        user = User(
            id="usr_b8_participant",
            email="b8_part@example.com",
            name="Batch 8 Participant",
            role="PARTICIPANT",
            hashed_password=get_password_hash("password123")
        )
        db.add(user)

    db.commit()
    db.close()

    return {
        "hackathon_id": "hack_b8_test",
        "user_id": "usr_b8_participant"
    }


def test_registration_and_audit(setup_b8_fixtures):
    f = setup_b8_fixtures
    payload = {"hackathon_id": f["hackathon_id"]}

    res = client.post("/api/v1/registrations", json=payload, headers={"Authorization": f["user_id"]})
    assert res.status_code == 201
    reg = res.json()
    assert reg["hackathon_id"] == f["hackathon_id"]
    assert reg["user_id"] == f["user_id"]
    reg_id = reg["id"]

    # Verify registration in list
    res_list = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/registrations")
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

    # Payment Checkout
    pay_payload = {
        "registration_id": reg_id,
        "amount": 49.99,
        "currency": "USD"
    }
    res_pay = client.post("/api/v1/payments/checkout", json=pay_payload, headers={"Authorization": f["user_id"]})
    assert res_pay.status_code == 201
    pay_id = res_pay.json()["id"]

    # Webhook Confirmation
    webhook_payload = {
        "payment_id": pay_id,
        "transaction_id": "tx_b8_12345",
        "success": True
    }
    res_wb = client.post("/api/v1/payments/webhook", json=webhook_payload)
    assert res_wb.status_code == 200
    assert res_wb.json()["status"] == "SUCCESS"

    # Query Audit Logs
    res_audit = client.get(f"/api/v1/audit-logs?hackathon_id={f['hackathon_id']}", headers={"Authorization": f["user_id"]})
    assert res_audit.status_code == 200
    logs = res_audit.json()
    actions = [l["action"] for l in logs]
    assert "USER_REGISTERED" in actions
    assert "PAYMENT_SUCCESS" in actions
