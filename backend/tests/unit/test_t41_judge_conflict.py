import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import Hackathon, User, Submission, Judge
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, UserRole, SubmissionStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_t41_fixtures():
    db = SessionLocal()

    uid = uuid.uuid4().hex[:6]
    hack_id = f"hack_t41_{uid}"
    hack = Hackathon(id=hack_id, name="T41 Conflict Hackathon", status=HackathonStatus.ACTIVE)
    db.add(hack)

    # Submission
    sub_id = f"sub_t41_{uid}"
    sub = Submission(id=sub_id, hackathon_id=hack_id, team_id=f"tm_t41_{uid}", title="Project T41", status=SubmissionStatus.SUBMITTED)
    db.add(sub)

    # Judge User
    j_user_id = f"usr_t41_j_{uid}"
    j_user = User(id=j_user_id, email=f"j_{uid}@example.com", name="Judge T41", role=UserRole.JUDGE, hashed_password=get_password_hash("password"))
    db.add(j_user)

    j_profile = Judge(id=f"jdg_t41_{uid}", user_id=j_user_id, hackathon_id=hack_id)
    db.add(j_profile)

    # Organizer User
    org_user_id = f"usr_t41_org_{uid}"
    org_user = User(id=org_user_id, email=f"org_{uid}@example.com", name="Org T41", role=UserRole.ORGANIZER, hashed_password=get_password_hash("password"))
    db.add(org_user)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "submission_id": sub_id,
        "judge_user_id": j_user_id,
        "org_user_id": org_user_id
    }


def test_t41_conflict_flow(setup_t41_fixtures):
    f = setup_t41_fixtures

    # 1. Judge declares conflict
    res_dec = client.post(
        "/api/v1/judges/me/conflicts",
        json={"submission_id": f["submission_id"], "reason": "Co-worked with team lead"},
        headers={"Authorization": f["judge_user_id"]}
    )
    assert res_dec.status_code == 201
    conflict_data = res_dec.json()
    conflict_id = conflict_data["id"]
    assert conflict_data["status"] == "DECLARED"

    # 2. Judge lists my conflicts
    res_my = client.get("/api/v1/judges/me/conflicts", headers={"Authorization": f["judge_user_id"]})
    assert res_my.status_code == 200
    assert len(res_my.json()) >= 1

    # 3. Organizer lists hackathon conflicts
    res_hack = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/conflicts", headers={"Authorization": f["org_user_id"]})
    assert res_hack.status_code == 200
    assert len(res_hack.json()) >= 1

    # 4. Organizer resolves conflict
    res_res = client.post(f"/api/v1/judge-conflicts/{conflict_id}/resolve", headers={"Authorization": f["org_user_id"]})
    assert res_res.status_code == 200
    assert res_res.json()["status"] == "RESOLVED"
