from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.core.dependencies import get_current_user_optional, UserIdentity
from app.utils.enums import UserRole

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["project"] == settings.PROJECT_NAME


def test_mock_session_header_resolution():
    # Test organizer header resolution
    response = client.get("/health", headers={"Cookie": "session=org_7f2a"})
    assert response.status_code == 200


def test_user_identity_class():
    identity = UserIdentity(id="usr_01", email="test@example.com", role=UserRole.ORGANIZER)
    assert identity.id == "usr_01"
    assert identity.role == UserRole.ORGANIZER
