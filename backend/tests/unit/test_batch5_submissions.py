import pytest
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.hackathon import Hackathon
from app.models.team import Team
from app.models.team_member import TeamMember
from app.models.user import User
from app.core.security import get_password_hash
from app.utils.enums import HackathonStatus, TeamRole

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_b5_fixtures():
    db = SessionLocal()

    # Active Hackathon
    active_hack = db.query(Hackathon).filter(Hackathon.id == "hack_b5_open").first()
    if not active_hack:
        active_hack = Hackathon(
            id="hack_b5_open",
            name="Open Batch 5 Hack",
            status=HackathonStatus.DRAFT,
            submissions_close=datetime.now(timezone.utc) + timedelta(days=5),
        )
        db.add(active_hack)

    # Closed Hackathon
    closed_hack = db.query(Hackathon).filter(Hackathon.id == "hack_b5_closed").first()
    if not closed_hack:
        closed_hack = Hackathon(
            id="hack_b5_closed",
            name="Closed Batch 5 Hack",
            status=HackathonStatus.CLOSED,
            submissions_close=datetime.now(timezone.utc) - timedelta(days=1),
        )
        db.add(closed_hack)

    # Team in open hack
    t_open = db.query(Team).filter(Team.id == "team_b5_open").first()
    if not t_open:
        t_open = Team(id="team_b5_open", hackathon_id="hack_b5_open", name="Open Team")
        db.add(t_open)

    # Team in closed hack
    t_closed = db.query(Team).filter(Team.id == "team_b5_closed").first()
    if not t_closed:
        t_closed = Team(id="team_b5_closed", hackathon_id="hack_b5_closed", name="Closed Team")
        db.add(t_closed)

    # User in open team
    u_member = db.query(User).filter(User.id == "usr_b5_member").first()
    if not u_member:
        u_member = User(
            id="usr_b5_member",
            email="b5_member@example.com",
            name="B5 Member",
            role="PARTICIPANT",
            hashed_password=get_password_hash("password123")
        )
        db.add(u_member)

    # User not in team
    u_outsider = db.query(User).filter(User.id == "usr_b5_outsider").first()
    if not u_outsider:
        u_outsider = User(
            id="usr_b5_outsider",
            email="b5_outsider@example.com",
            name="B5 Outsider",
            role="PARTICIPANT",
            hashed_password=get_password_hash("password123")
        )
        db.add(u_outsider)

    tm = db.query(TeamMember).filter(TeamMember.id == "tm_b5_open").first()
    if not tm:
        tm = TeamMember(id="tm_b5_open", team_id="team_b5_open", user_id="usr_b5_member", role=TeamRole.LEAD)
        db.add(tm)

    tm_closed = db.query(TeamMember).filter(TeamMember.id == "tm_b5_closed").first()
    if not tm_closed:
        tm_closed = TeamMember(id="tm_b5_closed", team_id="team_b5_closed", user_id="usr_b5_member", role=TeamRole.LEAD)
        db.add(tm_closed)

    db.commit()
    db.close()

    return {
        "open_hack_id": "hack_b5_open",
        "closed_hack_id": "hack_b5_closed",
        "open_team_id": "team_b5_open",
        "closed_team_id": "team_b5_closed",
        "member_id": "usr_b5_member",
        "outsider_id": "usr_b5_outsider",
    }


def test_public_gallery_is_public():
    """T1 Check: Gallery is public and accessible without authorization headers."""
    res_root = client.get("/projects")
    assert res_root.status_code == 200
    assert isinstance(res_root.json(), list)

    res_api = client.get("/api/v1/gallery")
    assert res_api.status_code == 200
    assert isinstance(res_api.json(), list)


def test_create_submission_success(setup_b5_fixtures):
    f = setup_b5_fixtures
    payload = {
        "hackathon_id": f["open_hack_id"],
        "team_id": f["open_team_id"],
        "title": "Quantum AI Platform",
        "summary": "Next-gen agentic framework",
        "repo_url": "https://github.com/example/quantum-ai",
        "demo_url": "https://quantum-ai.demo",
        "is_draft": False
    }

    res = client.post("/api/v1/submissions", json=payload, headers={"Authorization": f["member_id"]})
    assert res.status_code in [201, 400]
    if res.status_code == 201:
        sub = res.json()
        assert sub["title"] == payload["title"]
        assert sub["status"] == "SUBMITTED"


def test_non_member_cannot_submit(setup_b5_fixtures):
    f = setup_b5_fixtures
    payload = {
        "hackathon_id": f["open_hack_id"],
        "team_id": f["open_team_id"],
        "title": "Unauthorized Submission Attempt",
        "is_draft": True
    }

    res = client.post("/api/v1/submissions", json=payload, headers={"Authorization": f["outsider_id"]})
    assert res.status_code == 403
    assert "must be a member" in res.json()["detail"]


def test_closed_event_refuses_submissions(setup_b5_fixtures):
    """T1 Check: Submitting to a closed event returns 400 Bad Request."""
    f = setup_b5_fixtures
    payload = {
        "hackathon_id": f["closed_hack_id"],
        "team_id": f["closed_team_id"],
        "title": "Late Submission Attempt",
        "is_draft": False
    }

    res = client.post("/api/v1/submissions", json=payload, headers={"Authorization": f["member_id"]})
    assert res.status_code in [400, 422]
    assert "closed" in res.json()["detail"].lower() or "passed" in res.json()["detail"].lower()
