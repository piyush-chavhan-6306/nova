import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import Hackathon, User, Submission
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, UserRole, SubmissionStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_t34_fixtures():
    db = SessionLocal()

    hack_id = "hack_t34_test"
    hack = db.query(Hackathon).filter(Hackathon.id == hack_id).first()
    if not hack:
        hack = Hackathon(id=hack_id, name="T34 Blind Review Hackathon", status=HackathonStatus.ACTIVE, blind_review_enabled=True)
        db.add(hack)

    sub_id = "sub_t34_p1"
    sub = db.query(Submission).filter(Submission.id == sub_id).first()
    if not sub:
        sub = Submission(id=sub_id, hackathon_id=hack_id, team_id="team_t34_secret", title="Secret Blind Project", status=SubmissionStatus.SUBMITTED)
        db.add(sub)

    # Judge User
    j_user_id = "usr_t34_judge"
    j_user = db.query(User).filter(User.id == j_user_id).first()
    if not j_user:
        j_user = User(id=j_user_id, email="j_t34@example.com", name="Judge T34", role=UserRole.JUDGE, hashed_password=get_password_hash("password"))
        db.add(j_user)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "submission_id": sub_id,
        "judge_user_id": j_user_id
    }


def test_t34_blind_review_masking(setup_t34_fixtures):
    f = setup_t34_fixtures

    # Request submission details as a judge
    res = client.get(f"/api/v1/submissions/{f['submission_id']}", headers={"Authorization": f["judge_user_id"]})
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == f["submission_id"]
    assert data["team_id"] == "ANONYMOUS"
