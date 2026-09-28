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
def setup_t33_fixtures():
    db = SessionLocal()

    uid = uuid.uuid4().hex[:6]
    hack_id = f"hack_t33_{uid}"
    hack = Hackathon(id=hack_id, name="T33 Calibration Hackathon", status=HackathonStatus.ACTIVE)
    db.add(hack)

    sub_id = f"sub_t33_ref_{uid}"
    sub = Submission(id=sub_id, hackathon_id=hack_id, team_id=f"team_t33_{uid}", title="Reference Project 1", status=SubmissionStatus.SUBMITTED)
    db.add(sub)

    # Organizer User
    org_user_id = f"usr_t33_org_{uid}"
    org_user = User(id=org_user_id, email=f"org_{uid}@example.com", name="Org T33", role=UserRole.ORGANIZER, hashed_password=get_password_hash("password"))
    db.add(org_user)

    # Judge User
    j_user_id = f"usr_t33_j_{uid}"
    j_user = User(id=j_user_id, email=f"j_{uid}@example.com", name="Judge T33", role=UserRole.JUDGE, hashed_password=get_password_hash("password"))
    db.add(j_user)

    j_profile = Judge(id=f"jdg_t33_{uid}", user_id=j_user_id, hackathon_id=hack_id)
    db.add(j_profile)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "submission_id": sub_id,
        "org_user_id": org_user_id,
        "judge_user_id": j_user_id,
        "judge_id": f"jdg_t33_{uid}"
    }


def test_t33_calibration_flow(setup_t33_fixtures):
    f = setup_t33_fixtures

    # 1. Organizer creates calibration set
    set_res = client.post(
        f"/api/v1/hackathons/{f['hackathon_id']}/calibration-sets",
        json={"name": "Round 1 Calibration"},
        headers={"Authorization": f["org_user_id"]}
    )
    assert set_res.status_code == 201
    set_id = set_res.json()["id"]

    # 2. Add reference project
    proj_res = client.post(
        f"/api/v1/calibration-sets/{set_id}/projects",
        json={"submission_id": f["submission_id"], "expected_score": 8.5},
        headers={"Authorization": f["org_user_id"]}
    )
    assert proj_res.status_code == 201
    assert proj_res.json()["expected_score"] == 8.5

    # 3. Judge evaluates reference project
    res_record = client.post(
        "/api/v1/calibration-results",
        json={
            "calibration_set_id": set_id,
            "submission_id": f["submission_id"],
            "score": 8.0
        },
        headers={"Authorization": f["judge_user_id"]}
    )
    assert res_record.status_code == 201
    rec_data = res_record.json()
    assert rec_data["deviation"] == 0.5

    # 4. Check judge's calibration summary
    res_summary = client.get(
        f"/api/v1/judges/me/calibration?hackathon_id={f['hackathon_id']}",
        headers={"Authorization": f["judge_user_id"]}
    )
    assert res_summary.status_code == 200
    summary = res_summary.json()
    assert summary["total_calibrated"] == 1
    assert summary["average_deviation"] == 0.5
