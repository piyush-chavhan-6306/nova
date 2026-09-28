import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import Hackathon, User, Submission, Judge, PairwiseEvaluation
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, UserRole, SubmissionStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_t32_fixtures():
    db = SessionLocal()

    uid = uuid.uuid4().hex[:6]
    hack_id = f"hack_t32_{uid}"
    hack = Hackathon(id=hack_id, name="T32 Pairwise Hackathon", status=HackathonStatus.ACTIVE)
    db.add(hack)

    sub_a_id = f"sub_t32_a_{uid}"
    sub_b_id = f"sub_t32_b_{uid}"
    sub_a = Submission(id=sub_a_id, hackathon_id=hack_id, team_id=f"team_a_{uid}", title="Project A", status=SubmissionStatus.SUBMITTED)
    sub_b = Submission(id=sub_b_id, hackathon_id=hack_id, team_id=f"team_b_{uid}", title="Project B", status=SubmissionStatus.SUBMITTED)
    db.add(sub_a)
    db.add(sub_b)

    j_user_id = f"usr_t32_{uid}"
    j_user = User(id=j_user_id, email=f"j_{uid}@example.com", name="Judge T32", role=UserRole.JUDGE, hashed_password=get_password_hash("password"))
    db.add(j_user)

    j_profile = Judge(id=f"jdg_t32_{uid}", user_id=j_user_id, hackathon_id=hack_id)
    db.add(j_profile)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "submission_a_id": sub_a_id,
        "submission_b_id": sub_b_id,
        "judge_user_id": j_user_id,
        "judge_id": f"jdg_t32_{uid}"
    }


def test_t32_pairwise_flow(setup_t32_fixtures):
    f = setup_t32_fixtures

    # 1. Create evaluation
    payload = {
        "hackathon_id": f["hackathon_id"],
        "submission_a_id": f["submission_a_id"],
        "submission_b_id": f["submission_b_id"]
    }
    res_create = client.post("/api/v1/pairwise-evaluations", json=payload, headers={"Authorization": f["judge_user_id"]})
    assert res_create.status_code == 201
    eval_data = res_create.json()
    eval_id = eval_data["id"]
    assert eval_data["status"] == "ASSIGNED"

    # 2. Update winner
    update_payload = {
        "winner_submission_id": f["submission_a_id"],
        "reason": "Better UI/UX and core architecture"
    }
    res_upd = client.put(f"/api/v1/pairwise-evaluations/{eval_id}", json=update_payload, headers={"Authorization": f["judge_user_id"]})
    assert res_upd.status_code == 200
    assert res_upd.json()["winner_submission_id"] == f["submission_a_id"]

    # 3. Submit evaluation
    res_sub = client.post(f"/api/v1/pairwise-evaluations/{eval_id}/submit", headers={"Authorization": f["judge_user_id"]})
    assert res_sub.status_code == 200
    assert res_sub.json()["status"] == "SUBMITTED"

    # 4. Check progress
    res_prog = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/pairwise-progress", headers={"Authorization": f["judge_user_id"]})
    assert res_prog.status_code == 200
    prog = res_prog.json()
    assert prog["total_pairs"] == 1
    assert prog["completed_pairs"] == 1
