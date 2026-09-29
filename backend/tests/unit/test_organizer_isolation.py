import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.hackathon import Hackathon
from app.models.user import User
from app.models.track import Track
from app.utils.enums import UserRole, HackathonStatus
from app.core.security import get_password_hash

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_isolation_fixtures():
    db = SessionLocal()

    # Create Organizer A
    org_a = db.query(User).filter(User.id == "usr_org_a").first()
    if not org_a:
        org_a = User(
            id="usr_org_a",
            email="org_a@example.com",
            name="Organizer A",
            role=UserRole.ORGANIZER,
            hashed_password=get_password_hash("password123")
        )
        db.add(org_a)

    # Create Organizer B
    org_b = db.query(User).filter(User.id == "usr_org_b").first()
    if not org_b:
        org_b = User(
            id="usr_org_b",
            email="org_b@example.com",
            name="Organizer B",
            role=UserRole.ORGANIZER,
            hashed_password=get_password_hash("password123")
        )
        db.add(org_b)

    # Create Admin
    admin_user = db.query(User).filter(User.id == "usr_admin_test").first()
    if not admin_user:
        admin_user = User(
            id="usr_admin_test",
            email="admin@example.com",
            name="Platform Admin",
            role=UserRole.ADMIN,
            hashed_password=get_password_hash("password123")
        )
        db.add(admin_user)

    # Create Hackathon owned by Organizer A
    hack_a = db.query(Hackathon).filter(Hackathon.id == "hack_org_a_event").first()
    if not hack_a:
        hack_a = Hackathon(
            id="hack_org_a_event",
            name="Alpha AI Challenge",
            description="Organizer A exclusive event",
            status=HackathonStatus.ACTIVE,
            organizer_id="usr_org_a"
        )
        db.add(hack_a)

    # Create Hackathon owned by Organizer B
    hack_b = db.query(Hackathon).filter(Hackathon.id == "hack_org_b_event").first()
    if not hack_b:
        hack_b = Hackathon(
            id="hack_org_b_event",
            name="Beta Quantum Hackathon",
            description="Organizer B exclusive event",
            status=HackathonStatus.ACTIVE,
            organizer_id="usr_org_b"
        )
        db.add(hack_b)

    db.commit()
    db.close()

    return {
        "org_a_id": "usr_org_a",
        "org_b_id": "usr_org_b",
        "admin_id": "usr_admin_test",
        "hack_a_id": "hack_org_a_event",
        "hack_b_id": "hack_org_b_event",
    }


def test_organizer_cannot_edit_other_organizer_hackathon(setup_isolation_fixtures):
    f = setup_isolation_fixtures
    # Organizer B tries to update Organizer A's hackathon -> 403 Forbidden
    payload = {"name": "Hacked Alpha Title"}
    res = client.put(
        f"/api/v1/hackathons/{f['hack_a_id']}",
        json=payload,
        headers={"Authorization": f["org_b_id"]}
    )
    assert res.status_code == 403
    assert "Access denied" in res.json()["detail"]

    # Organizer A can update own hackathon -> 200 OK
    res_ok = client.put(
        f"/api/v1/hackathons/{f['hack_a_id']}",
        json={"name": "Alpha AI Challenge Updated"},
        headers={"Authorization": f["org_a_id"]}
    )
    assert res_ok.status_code == 200


def test_organizer_cannot_view_other_organizer_analytics(setup_isolation_fixtures):
    f = setup_isolation_fixtures
    # Organizer A tries to view Organizer B's analytics -> 403 Forbidden
    res = client.get(
        f"/api/v1/hackathons/{f['hack_b_id']}/analytics/submissions",
        headers={"Authorization": f["org_a_id"]}
    )
    assert res.status_code == 403

    # Organizer B can view own analytics -> 200 OK
    res_ok = client.get(
        f"/api/v1/hackathons/{f['hack_b_id']}/analytics/submissions",
        headers={"Authorization": f["org_b_id"]}
    )
    assert res_ok.status_code == 200


def test_organizer_cannot_run_integrity_checks_on_other_organizer_hackathon(setup_isolation_fixtures):
    f = setup_isolation_fixtures
    # Organizer B tries to run integrity checks on Hackathon A -> 403 Forbidden
    res = client.get(
        f"/api/v1/hackathons/{f['hack_a_id']}/integrity/checks",
        headers={"Authorization": f["org_b_id"]}
    )
    assert res.status_code == 403


def test_organizer_cannot_export_other_organizer_data(setup_isolation_fixtures):
    f = setup_isolation_fixtures
    # Organizer A tries to export Organizer B's judging CSV -> 403 Forbidden
    res = client.get(
        f"/api/v1/hackathons/{f['hack_b_id']}/exports/judging.csv",
        headers={"Authorization": f["org_a_id"]}
    )
    assert res.status_code == 403

    # Organizer A tries to export Organizer B's results CSV -> 403 Forbidden
    res_res = client.get(
        f"/api/v1/hackathons/{f['hack_b_id']}/exports/results.csv",
        headers={"Authorization": f["org_a_id"]}
    )
    assert res_res.status_code == 403


def test_organizer_cannot_view_other_organizer_sub_resources(setup_isolation_fixtures):
    f = setup_isolation_fixtures
    # Organizer A tries to view Hackathon B's registrations -> 403 Forbidden
    res_reg = client.get(
        f"/api/v1/hackathons/{f['hack_b_id']}/registrations",
        headers={"Authorization": f["org_a_id"]}
    )
    assert res_reg.status_code == 403

    # Organizer A tries to view Hackathon B's teams -> 403 Forbidden
    res_team = client.get(
        f"/api/v1/hackathons/{f['hack_b_id']}/teams",
        headers={"Authorization": f["org_a_id"]}
    )
    assert res_team.status_code == 403

    # Organizer A tries to view Hackathon B's assignments -> 403 Forbidden
    res_asgn = client.get(
        f"/api/v1/hackathons/{f['hack_b_id']}/assignments",
        headers={"Authorization": f["org_a_id"]}
    )
    assert res_asgn.status_code == 403


def test_organizer_cannot_view_other_organizer_audit_logs(setup_isolation_fixtures):
    f = setup_isolation_fixtures
    # Organizer A tries to view Hackathon B audit logs -> 403 Forbidden
    res = client.get(
        f"/api/v1/audit-logs?hackathon_id={f['hack_b_id']}",
        headers={"Authorization": f["org_a_id"]}
    )
    assert res.status_code == 403


def test_admin_can_access_all_organizer_hackathons(setup_isolation_fixtures):
    f = setup_isolation_fixtures
    # Admin can view Hackathon A analytics -> 200 OK
    res_a = client.get(
        f"/api/v1/hackathons/{f['hack_a_id']}/analytics/submissions",
        headers={"Authorization": f["admin_id"]}
    )
    assert res_a.status_code == 200

    # Admin can view Hackathon B analytics -> 200 OK
    res_b = client.get(
        f"/api/v1/hackathons/{f['hack_b_id']}/analytics/submissions",
        headers={"Authorization": f["admin_id"]}
    )
    assert res_b.status_code == 200


def test_judge_peer_isolation_enforced():
    # Judge B tries to inspect Judge A (jdg_01)'s raw scores -> 403 Forbidden
    res = client.get(
        "/api/v1/judging/scores?judge=jdg_01",
        headers={"Cookie": "session=jdg_b_44de"}
    )
    assert res.status_code == 403
    assert "Access denied" in res.json()["detail"]


def test_participant_cannot_execute_organizer_action(setup_isolation_fixtures):
    f = setup_isolation_fixtures
    # Participant tries to create a track on Hackathon A -> 403 Forbidden
    payload = {"name": "Unauthorized Track", "description": "Illegal track"}
    res = client.post(
        f"/api/v1/hackathons/{f['hack_a_id']}/tracks",
        json=payload,
        headers={"Cookie": "session=prt_2e88"}
    )
    assert res.status_code == 403


def test_hackathon_discovery_search_and_filter(setup_isolation_fixtures):
    # Public keyword search for "Alpha"
    res_search = client.get("/api/v1/hackathons?search=Alpha")
    assert res_search.status_code == 200
    results = res_search.json()
    assert len(results) >= 1
    assert "Alpha" in results[0]["name"]

    # Public filter by status "ACTIVE"
    res_filter = client.get("/api/v1/hackathons?status=ACTIVE")
    assert res_filter.status_code == 200
    for h in res_filter.json():
        assert h["status"] == "ACTIVE"


def test_t2_rubric_and_judge_management_isolation(setup_isolation_fixtures):
    f = setup_isolation_fixtures

    # 1. Organizer A creates a rubric for Hackathon A
    res_rubric = client.post(
        f"/api/v1/hackathons/{f['hack_a_id']}/rubrics",
        json={"name": "Alpha Custom Rubric"},
        headers={"Authorization": f["org_a_id"]}
    )
    assert res_rubric.status_code == 201
    rubric_id = res_rubric.json()["id"]

    # 2. Organizer B attempts to modify Organizer A's rubric -> 403 Forbidden
    res_b_mod = client.put(
        f"/api/v1/rubrics/{rubric_id}",
        json={"name": "Hacked Rubric Name"},
        headers={"Authorization": f["org_b_id"]}
    )
    assert res_b_mod.status_code == 403

    # 3. Organizer A adds criterion to rubric
    res_crit = client.post(
        f"/api/v1/rubrics/{rubric_id}/criteria",
        json={"name": "Technical Execution", "weight": 2.0, "max_score": 10.0},
        headers={"Authorization": f["org_a_id"]}
    )
    assert res_crit.status_code == 201
    crit_id = res_crit.json()["id"]
    assert res_crit.json()["weight"] == 2.0

    # 4. Organizer B attempts to delete Organizer A's criterion -> 403 Forbidden
    res_b_del_crit = client.delete(
        f"/api/v1/rubric-criteria/{crit_id}",
        headers={"Authorization": f["org_b_id"]}
    )
    assert res_b_del_crit.status_code == 403

    # 5. Organizer A invites/adds a judge to Hackathon A
    res_judge = client.post(
        f"/api/v1/hackathons/{f['hack_a_id']}/judges",
        json={"user_id": f["admin_id"], "title": "Guest Admin Judge"},
        headers={"Authorization": f["org_a_id"]}
    )
    assert res_judge.status_code == 201
    judge_id = res_judge.json()["id"]

    # 6. Organizer B attempts to delete Organizer A's judge -> 403 Forbidden
    res_b_del_judge = client.delete(
        f"/api/v1/judges/{judge_id}",
        headers={"Authorization": f["org_b_id"]}
    )
    assert res_b_del_judge.status_code == 403

    # 7. Organizer A deletes their criterion and judge cleanly -> 204
    res_a_del_crit = client.delete(
        f"/api/v1/rubric-criteria/{crit_id}",
        headers={"Authorization": f["org_a_id"]}
    )
    assert res_a_del_crit.status_code == 204

