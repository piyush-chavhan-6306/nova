import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models import Hackathon, User, Submission, Judge, JudgeAssignment
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, UserRole, SubmissionStatus, AssignmentStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_t36_fixtures():
    db = SessionLocal()

    uid = uuid.uuid4().hex[:6]
    hack_id = f"hack_t36_{uid}"
    hack = Hackathon(id=hack_id, name="T36 Dashboard Hackathon", status=HackathonStatus.ACTIVE)
    db.add(hack)

    # Submissions
    sub1 = Submission(id=f"sub_t36_1_{uid}", hackathon_id=hack_id, team_id=f"tm1_{uid}", title="Project 1", status=SubmissionStatus.SUBMITTED)
    db.add(sub1)

    # Judge
    j_user_id = f"usr_t36_{uid}"
    j_user = User(id=j_user_id, email=f"j_{uid}@example.com", name="Judge T36", role=UserRole.JUDGE, hashed_password=get_password_hash("password"))
    db.add(j_user)

    j_profile = Judge(id=f"jdg_t36_{uid}", user_id=j_user_id, hackathon_id=hack_id)
    db.add(j_profile)

    # Assignment
    assign = JudgeAssignment(id=f"asg_t36_{uid}", judge_id=j_profile.id, submission_id=sub1.id, status=AssignmentStatus.ASSIGNED)
    db.add(assign)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "judge_user_id": j_user_id,
        "judge_id": f"jdg_t36_{uid}"
    }


def test_t36_judge_dashboard_flow(setup_t36_fixtures):
    f = setup_t36_fixtures

    # 1. Get Judge Personal Dashboard
    res_dash = client.get(f"/api/v1/judges/me/dashboard?hackathon_id={f['hackathon_id']}", headers={"Authorization": f["judge_user_id"]})
    assert res_dash.status_code == 200
    dash = res_dash.json()
    assert dash["assigned_projects"] == 1
    assert dash["pending_reviews"] == 1
    assert dash["completion_percentage"] == 0.0

    # 2. Get Hackathon Judging Progress
    res_prog = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/judging-progress")
    assert res_prog.status_code == 200
    prog = res_prog.json()
    assert prog["total_submissions"] == 1
    assert prog["total_assignments"] == 1
    assert prog["pending_assignments"] == 1
    assert len(prog["judge_workload"]) >= 1
