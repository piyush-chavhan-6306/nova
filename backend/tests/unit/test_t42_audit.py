import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import Hackathon, User, AuditLog
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, UserRole

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_t42_fixtures():
    db = SessionLocal()

    uid = uuid.uuid4().hex[:6]
    hack_id = f"hack_t42_{uid}"
    hack = Hackathon(id=hack_id, name="T42 Audit Hackathon", status=HackathonStatus.ACTIVE)
    db.add(hack)

    # Organizer User
    org_user_id = f"usr_t42_org_{uid}"
    org_user = User(id=org_user_id, email=f"org_{uid}@example.com", name="Org T42", role=UserRole.ORGANIZER, hashed_password=get_password_hash("password"))
    db.add(org_user)

    # Audit log
    audit_id = f"aud_t42_{uid}"
    al = AuditLog(
        id=audit_id,
        hackathon_id=hack_id,
        user_id=org_user_id,
        action="RESULT_CALCULATED",
        target_type="hackathon",
        target_id=hack_id,
        details="Calculated hackathon results"
    )
    db.add(al)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "org_user_id": org_user_id,
        "audit_id": audit_id
    }


def test_t42_audit_trail_filters(setup_t42_fixtures):
    f = setup_t42_fixtures

    # 1. Query hackathon audit logs
    res1 = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/audit-logs", headers={"Authorization": f["org_user_id"]})
    assert res1.status_code == 200
    logs = res1.json()
    assert len(logs) >= 1

    # 2. Query with action filter
    res2 = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/audit-logs?action=RESULT_CALCULATED", headers={"Authorization": f["org_user_id"]})
    assert res2.status_code == 200
    assert len(res2.json()) >= 1
