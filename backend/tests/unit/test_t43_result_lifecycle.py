import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import Hackathon, User, Submission
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, UserRole, SubmissionStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_t43_fixtures():
    db = SessionLocal()

    uid = uuid.uuid4().hex[:6]
    hack_id = f"hack_t43_{uid}"
    hack = Hackathon(id=hack_id, name="T43 Lifecycle Hackathon", status=HackathonStatus.ACTIVE)
    db.add(hack)

    # Submissions
    sub1 = Submission(id=f"sub_t43_1_{uid}", hackathon_id=hack_id, team_id=f"tm1_{uid}", title="Project 1", status=SubmissionStatus.SUBMITTED)
    db.add(sub1)

    # Organizer User
    org_user_id = f"usr_t43_org_{uid}"
    org_user = User(id=org_user_id, email=f"org_{uid}@example.com", name="Org T43", role=UserRole.ORGANIZER, hashed_password=get_password_hash("password"))
    db.add(org_user)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "org_user_id": org_user_id
    }


def test_t43_result_lifecycle_flow(setup_t43_fixtures):
    f = setup_t43_fixtures

    # 1. Calculate results
    res_calc = client.post(f"/api/v1/hackathons/{f['hackathon_id']}/results/calculate", headers={"Authorization": f["org_user_id"]})
    assert res_calc.status_code == 200

    # 2. Transition to Under Review
    res_rev = client.post(f"/api/v1/hackathons/{f['hackathon_id']}/results/review", headers={"Authorization": f["org_user_id"]})
    assert res_rev.status_code == 200

    # 3. Approve results
    res_app = client.post(f"/api/v1/hackathons/{f['hackathon_id']}/results/approve", headers={"Authorization": f["org_user_id"]})
    assert res_app.status_code == 200

    # 4. Publish results
    res_pub = client.post(f"/api/v1/hackathons/{f['hackathon_id']}/results/publish", headers={"Authorization": f["org_user_id"]})
    assert res_pub.status_code == 200

    # 5. Lock results
    res_lock = client.post(f"/api/v1/hackathons/{f['hackathon_id']}/results/lock", headers={"Authorization": f["org_user_id"]})
    assert res_lock.status_code == 200

    # 6. Attempt recalculation when locked -> Should fail 403
    res_recalc = client.post(f"/api/v1/hackathons/{f['hackathon_id']}/results/calculate", headers={"Authorization": f["org_user_id"]})
    assert res_recalc.status_code == 403
