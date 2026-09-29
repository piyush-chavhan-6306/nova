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
def setup_t44_fixtures():
    db = SessionLocal()

    uid = uuid.uuid4().hex[:6]
    hack_id = f"hack_t44_{uid}"
    org_user_id = f"usr_t44_org_{uid}"
    org_user = User(id=org_user_id, email=f"org_{uid}@example.com", name="Org T44", role=UserRole.ORGANIZER, hashed_password=get_password_hash("password"))
    db.add(org_user)

    hack = Hackathon(id=hack_id, name="T44 Organizer Hackathon", status=HackathonStatus.ACTIVE, organizer_id=org_user_id)
    db.add(hack)

    # Submissions
    sub1 = Submission(id=f"sub_t44_1_{uid}", hackathon_id=hack_id, team_id=f"tm1_{uid}", title="Project 1", status=SubmissionStatus.SUBMITTED)
    db.add(sub1)

    db.commit()
    db.close()

    return {
        "hackathon_id": hack_id,
        "org_user_id": org_user_id
    }


def test_organizer_analytics_and_dashboard(setup_t44_fixtures):
    f = setup_t44_fixtures

    # 1. Submission Analytics
    res_sub_ana = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/analytics/submissions", headers={"Authorization": f["org_user_id"]})
    assert res_sub_ana.status_code == 200
    assert res_sub_ana.json()["total_submissions"] == 1

    # 2. Judging Analytics
    res_jdg_ana = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/analytics/judging", headers={"Authorization": f["org_user_id"]})
    assert res_jdg_ana.status_code == 200

    # 3. Track Analytics
    res_trk_ana = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/analytics/tracks", headers={"Authorization": f["org_user_id"]})
    assert res_trk_ana.status_code == 200

    # 4. Integrity Checks
    res_integ = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/integrity/checks", headers={"Authorization": f["org_user_id"]})
    assert res_integ.status_code == 200
    assert "alerts_count" in res_integ.json()

    # 5. Organizer Dashboard
    res_dash = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/organizer/dashboard", headers={"Authorization": f["org_user_id"]})
    assert res_dash.status_code == 200
    dash = res_dash.json()
    assert "registrations" in dash
    assert "submissions" in dash

    # 6. Advanced CSV Exports
    res_exp1 = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/exports/results.csv")
    assert res_exp1.status_code == 200
    assert "Rank" in res_exp1.text

    res_exp2 = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/exports/judging.csv", headers={"Authorization": f["org_user_id"]})
    assert res_exp2.status_code == 200
    assert "Review ID" in res_exp2.text

    res_exp3 = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/exports/judges.csv", headers={"Authorization": f["org_user_id"]})
    assert res_exp3.status_code == 200
    assert "Judge ID" in res_exp3.text

    res_exp4 = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/exports/audit.csv", headers={"Authorization": f["org_user_id"]})
    assert res_exp4.status_code == 200
    assert "Audit ID" in res_exp4.text

    res_exp5 = client.get(f"/api/v1/hackathons/{f['hackathon_id']}/exports/integrity.csv", headers={"Authorization": f["org_user_id"]})
    assert res_exp5.status_code == 200
    assert "Alert Type" in res_exp5.text
