import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import Hackathon, User, Track, Submission, Judge, JudgeTrack
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, UserRole, SubmissionStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_t31_fixtures():
    db = SessionLocal()

    hack_id = "hack_t31_test"
    hack = db.query(Hackathon).filter(Hackathon.id == hack_id).first()
    if not hack:
        hack = Hackathon(id=hack_id, name="T31 Test Hackathon", status=HackathonStatus.ACTIVE)
        db.add(hack)

    track_id = "trk_t31_ai"
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        track = Track(id=track_id, hackathon_id=hack_id, name="AI Track")
        db.add(track)

    sub_id = "sub_t31_p1"
    sub = db.query(Submission).filter(Submission.id == sub_id).first()
    if not sub:
        sub = Submission(
            id=sub_id,
            hackathon_id=hack_id,
            team_id="team_t31_p1",
            track_id=track_id,
            title="T31 AI Project",
            status=SubmissionStatus.SUBMITTED
        )
        db.add(sub)

    # Judge user
    j_user_id = "usr_t31_j1"
    j_user = db.query(User).filter(User.id == j_user_id).first()
    if not j_user:
        j_user = User(
            id=j_user_id,
            email="j1_t31@example.com",
            name="Judge T31 One",
            role=UserRole.JUDGE,
            hashed_password=get_password_hash("password")
        )
        db.add(j_user)

    judge_id = "jdg_t31_j1"
    judge = db.query(Judge).filter(Judge.id == judge_id).first()
    if not judge:
        judge = Judge(id=judge_id, user_id=j_user_id, hackathon_id=hack_id, title="Expert Judge")
        db.add(judge)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "track_id": track_id,
        "submission_id": sub_id,
        "judge_id": judge_id,
        "judge_user_id": j_user_id
    }


def test_t31_single_assignment_and_delete(setup_t31_fixtures):
    f = setup_t31_fixtures
    payload = {
        "submission_id": f["submission_id"],
        "judge_id": f["judge_id"],
        "assignment_round": 1
    }

    # Create assignment
    res = client.post("/api/v1/judge-assignments", json=payload, headers={"Authorization": f["judge_user_id"]})
    assert res.status_code == 201
    data = res.json()
    assert data["judge_id"] == f["judge_id"]
    assert data["submission_id"] == f["submission_id"]
    assert data["status"] == "ASSIGNED"
    asgn_id = data["id"]

    # Retrieve assignments for hackathon
    res_list = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/assignments", headers={"Authorization": f["judge_user_id"]})
    assert res_list.status_code == 200
    assert any(a["id"] == asgn_id for a in res_list.json())

    # Delete assignment
    res_del = client.delete(f"/api/v1/judge-assignments/{asgn_id}", headers={"Authorization": f["judge_user_id"]})
    assert res_del.status_code == 204


def test_t31_batch_assignment(setup_t31_fixtures):
    f = setup_t31_fixtures
    batch_payload = {
        "hackathon_id": f["hackathon_id"],
        "target_reviews_per_project": 1,
        "assignment_round": 1
    }

    res_batch = client.post("/api/v1/judge-assignments/batch", json=batch_payload, headers={"Authorization": f["judge_user_id"]})
    assert res_batch.status_code == 201
    assigned = res_batch.json()
    assert isinstance(assigned, list)
