import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_auth_registration_and_login():
    email = "new_user_test@example.com"
    register_payload = {
        "email": email,
        "password": "TestPassword123!",
        "name": "Test User",
        "role": "PARTICIPANT"
    }

    # Register
    res_reg = client.post("/api/v1/auth/register", json=register_payload)
    assert res_reg.status_code in [201, 400]  # 400 if already exists from prior runs

    # Login
    login_payload = {
        "email": email,
        "password": "TestPassword123!"
    }
    res_login = client.post("/api/v1/auth/login", json=login_payload)
    assert res_login.status_code == 200
    data = res_login.json()
    assert "access_token" in data
    assert data["role"] == "PARTICIPANT"

    token = data["access_token"]

    # Access /users/me using Bearer token
    res_me = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    assert res_me.json()["email"] == email


def test_mock_session_headers_auth():
    # Test fixture/mock organizer cookie header
    res_organizer = client.get("/api/v1/users/me", headers={"Cookie": "session=org_7f2a"})
    assert res_organizer.status_code == 200
    assert res_organizer.json()["role"] == "ORGANIZER"

    # Test fixture/mock participant cookie header
    res_part = client.get("/api/v1/users/me", headers={"Cookie": "session=prt_2e88"})
    assert res_part.status_code == 200
    assert res_part.json()["role"] == "PARTICIPANT"


def test_users_rbac():
    # Participant should be forbidden from listing all users
    res_forbidden = client.get("/api/v1/users", headers={"Cookie": "session=prt_2e88"})
    assert res_forbidden.status_code == 403

    # Organizer should be allowed to list users
    res_allowed = client.get("/api/v1/users", headers={"Cookie": "session=org_7f2a"})
    assert res_allowed.status_code == 200
    assert isinstance(res_allowed.json(), list)


def test_hackathon_and_track_management():
    # 1. Create Hackathon as Organizer
    hackathon_payload = {
        "name": "Batch 3 Test Hackathon",
        "description": "Testing Batch 3 APIs",
        "status": "DRAFT",
        "max_team_size": 4,
        "min_team_size": 1
    }
    res_create = client.post(
        "/api/v1/hackathons",
        json=hackathon_payload,
        headers={"Cookie": "session=org_7f2a"}
    )
    assert res_create.status_code == 201
    h_data = res_create.json()
    h_id = h_data["id"]
    assert h_data["name"] == hackathon_payload["name"]

    # 2. List Hackathons
    res_list = client.get("/api/v1/hackathons")
    assert res_list.status_code == 200
    assert len(res_list.json()) > 0

    # 3. Create Track under Hackathon
    track_payload = {
        "name": "AI Innovation Track",
        "description": "Build agentic AI systems"
    }
    res_track = client.post(
        f"/api/v1/hackathons/{h_id}/tracks",
        json=track_payload,
        headers={"Cookie": "session=org_7f2a"}
    )
    assert res_track.status_code == 201
    t_data = res_track.json()
    assert t_data["name"] == track_payload["name"]

    # 4. Get Hackathon detail with tracks
    res_detail = client.get(f"/api/v1/hackathons/{h_id}")
    assert res_detail.status_code == 200
    detail_data = res_detail.json()
    assert len(detail_data["tracks"]) >= 1
    assert detail_data["tracks"][0]["name"] == track_payload["name"]
