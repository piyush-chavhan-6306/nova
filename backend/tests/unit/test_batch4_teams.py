import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.hackathon import Hackathon
from app.models.user import User
from app.core.security import get_password_hash

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_test_event_and_users():
    db = SessionLocal()
    # Ensure a hackathon exists
    hackathon = db.query(Hackathon).first()
    if not hackathon:
        hackathon = Hackathon(
            id="hack_b4_test",
            name="Batch 4 Hackathon",
            min_team_size=1,
            max_team_size=4,
        )
        db.add(hackathon)
        db.commit()
        db.refresh(hackathon)
    
    # Create test user 1 (Inviter / Lead)
    u1 = db.query(User).filter(User.email == "b4_lead@example.com").first()
    if not u1:
        u1 = User(
            id="usr_b4_lead",
            email="b4_lead@example.com",
            name="Batch 4 Lead",
            role="PARTICIPANT",
            hashed_password=get_password_hash("password123")
        )
        db.add(u1)

    # Create test user 2 (Invitee / Member)
    u2 = db.query(User).filter(User.email == "b4_member@example.com").first()
    if not u2:
        u2 = User(
            id="usr_b4_member",
            email="b4_member@example.com",
            name="Batch 4 Member",
            role="PARTICIPANT",
            hashed_password=get_password_hash("password123")
        )
        db.add(u2)

    db.commit()
    h_id = hackathon.id
    u1_id = u1.id
    u2_id = u2.id
    db.close()

    return {"hackathon_id": h_id, "lead_id": u1_id, "member_id": u2_id}


def test_create_team(setup_test_event_and_users):
    data = setup_test_event_and_users
    h_id = data["hackathon_id"]
    lead_id = data["lead_id"]

    payload = {
        "hackathon_id": h_id,
        "name": "Super AI Builders"
    }

    res = client.post("/api/v1/teams", json=payload, headers={"Authorization": lead_id})
    assert res.status_code in [201, 400]
    if res.status_code == 201:
        team = res.json()
        assert team["name"] == "Super AI Builders"
        assert len(team["members"]) == 1
        assert team["members"][0]["user_id"] == lead_id
        assert team["members"][0]["role"] == "LEAD"


def test_prevent_duplicate_team_in_hackathon(setup_test_event_and_users):
    data = setup_test_event_and_users
    h_id = data["hackathon_id"]
    lead_id = data["lead_id"]

    payload = {
        "hackathon_id": h_id,
        "name": "Second Team Attempt"
    }
    res = client.post("/api/v1/teams", json=payload, headers={"Authorization": lead_id})
    assert res.status_code == 400
    assert "already part of a team" in res.json()["detail"]


def test_team_invitation_flow(setup_test_event_and_users):
    data = setup_test_event_and_users
    h_id = data["hackathon_id"]
    lead_id = data["lead_id"]
    member_id = data["member_id"]

    # 1. Get lead team (the team where lead_id is member)
    res_teams = client.get(f"/api/v1/hackathons/{h_id}/teams")
    assert res_teams.status_code == 200
    teams = res_teams.json()
    
    my_team = None
    for t in teams:
        for m in t["members"]:
            if m["user_id"] == lead_id:
                my_team = t
                break
        if my_team:
            break

    assert my_team is not None
    team_id = my_team["id"]

    # 2. Invite member by email
    invite_payload = {"email": "b4_member@example.com"}
    res_inv = client.post(f"/api/v1/teams/{team_id}/invites", json=invite_payload, headers={"Authorization": lead_id})
    assert res_inv.status_code == 201
    invitation = res_inv.json()
    assert invitation["status"] == "PENDING"
    inv_id = invitation["id"]

    # 3. Non-lead tries to invite -> 403
    res_forbidden = client.post(f"/api/v1/teams/{team_id}/invites", json=invite_payload, headers={"Authorization": member_id})
    assert res_forbidden.status_code == 403

    # 4. Invitee accepts invitation
    respond_payload = {"accept": True}
    res_accept = client.post(f"/api/v1/teams/invites/{inv_id}/respond", json=respond_payload, headers={"Authorization": member_id})
    assert res_accept.status_code == 200
    assert res_accept.json()["status"] == "ACCEPTED"

    # 5. Verify team now has 2 members
    res_team = client.get(f"/api/v1/teams/{team_id}")
    assert res_team.status_code == 200
    updated_team = res_team.json()
    assert len(updated_team["members"]) == 2


def test_remove_team_member(setup_test_event_and_users):
    data = setup_test_event_and_users
    h_id = data["hackathon_id"]
    lead_id = data["lead_id"]
    member_id = data["member_id"]

    res_teams = client.get(f"/api/v1/hackathons/{h_id}/teams")
    teams = res_teams.json()
    
    my_team = None
    for t in teams:
        for m in t["members"]:
            if m["user_id"] == lead_id:
                my_team = t
                break
        if my_team:
            break

    assert my_team is not None
    team_id = my_team["id"]

    # Member leaves team
    res_remove = client.delete(f"/api/v1/teams/{team_id}/members/{member_id}", headers={"Authorization": member_id})
    assert res_remove.status_code == 200

    # Verify team has 1 member again
    res_team = client.get(f"/api/v1/teams/{team_id}")
    assert len(res_team.json()["members"]) == 1
